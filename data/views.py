import os

from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import data.algos
from django.http import Http404
from django.http import HttpResponseForbidden
from Vestivise import permission
from Vestivise import settings
from Vestivise.Vestivise import VestiviseException, QuovoWebhookException, network_response
from data.models import Holding, Account
from dashboard.models import QuovoUser
from Vestivise import mailchimp
from tasks import task_nightly_process
import logging
import json
from Vestivise.quovo import Quovo

def holdingEditor(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return render(request, "data/holdingEditorView.html")


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def testNightlyProcess(request):
    task_nightly_process()
    return network_response("success")

@api_view(["GET"])
def demoBroker(request, module):
    jsonFile = open(os.path.join(settings.BASE_DIR, 'data/fixtures/demoData.json'))
    demo_data = json.loads(jsonFile.read())
    if not demo_data.get(module):
        raise Http404
    return network_response(demo_data.get(module))

@api_view(["GET"])
@permission_classes((IsAuthenticated, permission.QuovoAccountPermission))
def broker(request, module):
    """
    Gets the output of the requested module.
    :param request: The request to be forwarded to the module algorithm.
    :param module: The name of the desired module algorithm.
    :return: The response produced by the desired module algorithm.
    """
    if not request.user.is_authenticated() and not "Test" in module:
        raise Http404("Please Log In before using data API")
    module = module
    if hasattr(data.algos, module):
        try:
            method = getattr(data.algos, module)
            return method(request)
        except Exception as e:
            logger = logging.getLogger('broker')
            logger.exception(e.message, exc_info=True)
            raise e
    else:
        raise Http404("Module not found")

class HoldingSerializer(generics.ListAPIView):
    serializer_class = Holding
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Holding.objects.all()

        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            queryset = Holding.objects.filter(cusip__isnull=True)

        return queryset

class HoldingDetailView(generics.UpdateAPIView):
    serializer_class = Holding
    permission_classes = (IsAdminUser,)
    queryset = Holding.objects.all()


logger = logging.getLogger('quovo_sync')
# WEBHOOK FINISH SYNC
@api_view(['POST'])
@permission_classes((permission.QuovoWebHookPermission, ))
def finishSyncHandler(request):
    data = request.data
    user = data.get("user")
    user_id = user.get("id")
    account = data.get("account")
    account_id = account.get("id")
    logger.info("begin quovo sync logging: " + json.dumps(request.data))
    if data.get("event") == "sync" and data.get("action") == "completed":
        try:
            handleNewQuovoSync(user_id, account_id)
        except VestiviseException as e:
            e.log_error()
            return e.generateErrorResponse()
    return network_response("")

def handleNewQuovoSync(quovo_id, account_id):
    try:
        vestivise_quovo_user = QuovoUser.objects.get(quovoID=quovo_id)
        # if the user has no current holdings it means that this is their first sync
        if not Account.objects.filter(quovoID=account_id).exists():
            holdings = Quovo.get_account_portfolios(account_id).get("portfolios")
            if holdings:
                logger.info("begin first time sync for: " + str(vestivise_quovo_user.id))
                vestivise_quovo_user.updateAccounts()
                vestivise_quovo_user.updatePortfolios()
                new_holdings = vestivise_quovo_user.getNewHoldings()
                vestivise_quovo_user.setCurrentHoldings(new_holdings)
                email = vestivise_quovo_user.userProfile.user.email
                mailchimp.sendProcessingHoldingNotification(email)
        else:
            a = Account.objects.get(quovoID=account_id)
            a.active = True
            a.save()
    except QuovoUser.DoesNotExist:
        raise QuovoWebhookException("User {0} does not exist".format(quovo_id))
