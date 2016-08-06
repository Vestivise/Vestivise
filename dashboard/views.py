from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import json
from rest_framework.decorators import api_view
import time
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.


# ROUTE VIEWS
def dashboard(request):
    if not request.user.is_authenticated():
        return redirect(reverse('loginView'))
    return render(request, "dashboard/dashboard.html")

def linkAccountPage(request):
    if not request.user.is_authenticated():
        return redirect(reverse('loginView'))
    return render(request, "dashboard/linkAccount.html")

def dataUpdatePage(request):
    if not request.user.is_authenticated():
        return redirect(reverse('loginView'))
    return render(request, "dashboard/updateData.html")

def homeRouter(request):
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return redirect(reverse('loginPage'))

# VIEW SETS







# TEST VIEWS
@api_view(('GET',))
def dashboardTestData(request):
    jsonFile = open(os.path.join(settings.BASE_DIR, 'dashboard/fixtures/basicAccountModel.json'))
    return JsonResponse(json.loads(jsonFile.read()))
