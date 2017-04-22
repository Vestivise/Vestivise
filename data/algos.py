import re

import math

from django.db.models import F
from django.db.models import Func
import numpy as np
import json
from django.utils.datetime_safe import datetime
from data.models import Holding, AverageUserReturns, AverageUserBondEquity, HoldingExpenseRatio, AverageUserSharpe, \
    AverageUserFee, Benchmark
from Vestivise.Vestivise import network_response

# CONSTANTS

AgeBenchDict = {2010: 'VTENX', 2020: 'VTWNX', 2030: 'VTHRX', 2040: 'VFORX',
                2050: 'VFIFX', 2060: 'VTTSX'}

BenchNameDict = {'VTENX': 'Vanguard Target Retirement 2010 Fund', 'VTWNX': 'Vanguard Target Retirement 2020 Fund',
                 'VTHRX': 'Vanguard Target Retirement 2030 Fund', 'VFORX': 'Vanguard Target Retirement 2040 Fund',
                 'VFIFX': 'Vanguard Target Retirement 2050 Fund', 'VTTSX': 'Vanguard Target Retirement 2060 Fund'}

# UTILITY FUNCTIONS

def ageMap(age):
    '''
    Maps the given age to an age group, represented by the upper end of it.
    The age group is then the result minus four to and including the result.
    :param age: Given age
    :return: Upper end of the age group.
    '''
    return age + (0 if age%5==0 else 5 - age%5)

# ALGOS

def riskReturnProfile(request, acctIgnore=None):
    """
    BASIC RISK MODULE:
    Returns the calculated Sharpe Ratio of the
    user's portfolio, using the shortest term
    treasury bond rate as risk free rate of
    return, and average vestivise user sharpe for user's age group

    OUTPUT:
    {
        'riskLevel': <float>
        'averageUser' : <float>
        'ageRange': <string>
    }

    """
    user = request.user
    profile = user.profile
    age = profile.get_age()
    if not acctIgnore:
        # Collect stored sharpe of user profile.
        sp = profile.quovoUser.userSharpes.latest('createdAt').value if user.profile.quovoUser.userSharpes.exists() else 0.0
    else:
        # Compute sharpe based on ignored accounts.
        tmp = profile.quovoUser.getUserSharpe(acctIgnore=acctIgnore)
        if not tmp:
            sp = 0
        else:
            sp = tmp.value

    ageGroup = ageMap(profile.get_age())
    if ageGroup < 20: ageGroup = 20
    elif ageGroup > 80: ageGroup = 80
    averageUserSharpes = 0.7

    try:
        # Collect average user sharpe ratio for this agegroup.
        averageUserSharpes = AverageUserSharpe.objects.filter(ageGroup__exact=ageGroup).latest('createdAt').mean
    except AverageUserSharpe.DoesNotExist:
        try:
        # Collect average user sharpe ratio among all users.
            averageUserSharpes = AverageUserSharpe.objects.filter(ageGroup__exact=0).latest('createdAt').mean
        except Exception:
            # It's okay we already set a default case of .7
            pass
    if averageUserSharpes == float("-inf") or averageUserSharpes == float("inf"):
        averageUserSharpes = 0.7

    bench = Benchmark.objects.annotate(abs_diff=Func(F('age_group') - age, function='ABS')).order_by('abs_diff').first()


    return network_response(
        {
            'riskLevel': round(sp, 2),
            'averageUser': round(averageUserSharpes, 2),
            'ageRange': "%s-%s" % (ageGroup-4, ageGroup)
        }
    )



def fees(request, acctIgnore=None):
    """
    BASIC COST MODULE:
    Returns the sum over the net expense ratios
    of the user's investment options.

    OUTPUT:
    A JSON containing only the aggregate net expense
    ratio.
    {
     'fee' : <float>,
     'averageFee': <float>,
     'averagePlacement': <string>
    }
    """

    holds = request.user.profile.quovoUser.getDisplayHoldings(acctIgnore=acctIgnore)
    totVal = sum([x.value for x in holds])
    weights = [x.value/totVal for x in holds]
    # Take dot product of weight vector and expense ratios of holdings.
    costRet = np.dot(weights, [x.holding.expenseRatios.latest('createdAt').expense for x in holds])
    try:
        auf = AverageUserFee.objects.latest('createdAt').avgFees
    except AverageUserFee.DoesNotExist:
        auf = .64
    if costRet < auf -.2:
        averagePlacement = 'less than'
    elif costRet > auf + .2:
        averagePlacement = 'more than'
    else:
        averagePlacement = 'similar to'
    return network_response({'fee': round(costRet, 2),
                             "averageFee": round(auf, 2),
                             'averagePlacement': averagePlacement})


def returns(request, acctIgnore=None):
    """
    BASIC RETURNS MODULE:
    Returns a list of all the historic returns
    associated with a user's investment options.

    OUTPUT:
    A JSON containing a list of all the
    historic returns associated with that
    investment option, keys are the symbol of that
    option.
    {'returns': <list of len 3>,
     'benchmark': <list of len 3>,
     'benchmarkName': <string>
    }
    """
    global AgeBenchDict
    profile = request.user.profile
    qu = profile.quovoUser
    try:
        returns = qu.getUserReturns(acctIgnore=acctIgnore)
    except Exception:
        returns = {'yearToDate': 0.0, 'twoYearReturns': 0.0, 'oneYearReturns': 0.0}
    dispReturns = [returns['yearToDate'], returns['oneYearReturns'], returns['twoYearReturns']]
    dispReturns = [round(x, 2) for x in dispReturns]

    age = profile.get_age()

    bench = Benchmark.objects.annotate(abs_diff=Func(F('age_group') - age, function='ABS')).order_by('abs_diff').first()
    bench_mark_returns = bench.get_returns_wrapped()
    benchRet = [
        bench_mark_returns["year_to_date"],
        bench_mark_returns["one_year"],
        bench_mark_returns["two_year"]
    ]
    benchRet = [round(x, 2) for x in benchRet]
    return network_response({
        "returns": dispReturns,
        "benchmark": benchRet,
        "benchmarkName": bench.name
    })



def holdingTypes(request, acctIgnore=None):
    """
    BASIC ASSETS MODULE:
    Returns the total amount invested in the holdings,
    and the percentage of the total amount invested
    in which type of holdings.

    OUTPUT:
    A JSON mapping 'percentages', to a dictionary
    of holdingTypes strings to their corresponding percentages,
    and 'totalInvested' to the total amount invested in
    the portfolio.
    {'percentages': {'realEstate': 75.00
                    'someOtherThing':25.00}
     'totalInvested': 100000,
     'holdingTypes' : 4
     }
    """
    resDict = {'StockLong': 0.0, 'StockShort': 0.0,
               'BondLong': 0.0, 'BondShort': 0.0,
               'CashLong': 0.0, 'CashShort': 0.0,
               'OtherLong': 0.0, 'OtherShort': 0.0}
    flipDict = {'StockLong' : 'StockShort', 'StockShort': 'StockLong',
                'BondLong': 'BondShort', 'BondShort': 'BondLong',
                'CashLong': 'CashShort', 'CashShort': 'CashLong',
                'OtherLong': 'OtherShort', 'OtherShort': 'OtherLong'}
    result = {
        'percentages': resDict,
        'totalInvested': round(0, 2),
        'holdingTypes': 0
    }
    holds = request.user.profile.quovoUser.getDisplayHoldings(acctIgnore=acctIgnore)

    if not holds: return network_response(result)

    totalVal = sum([x.value for x in holds])
    # Compile a list of dictionaries, each of which associate the type of asset
    # with its corresponding percentage towards the overall portfolio.
    breakDowns = [dict([(x.asset, x.percentage * h.value/totalVal)
                  for x in h.holding.assetBreakdowns.filter(updateIndex__exact=h.holding.currentUpdateIndex)])
                  for h in holds]
    # Keep totPercent as a normalizing constant
    # Compile all the percentages across our breakdowns
    # into the resDict. If the percentage is negative
    # treat it as the opposite. A short becomes a long, etc.
    totPercent = 0
    for breakDown in breakDowns:
        for kind in resDict:
            if kind in breakDown:
                if breakDown[kind] >= 0.0:
                    resDict[kind] += breakDown[kind]
                else:
                    resDict[flipDict[kind]] += abs(breakDown[kind])
                totPercent += abs(breakDown[kind])
    holdingTypes = 0
    kindMap = {
        "Stock" : False,
        "Bond": False,
        "Cash": False,
        "Other": False,
    }
    # Count the number of significant types.
    for kind in resDict:
        resDict[kind] = resDict[kind]/totPercent*100
        k = re.findall('[A-Z][^A-Z]*', kind)
        if resDict[kind] >= 0.5:
            if not kindMap.get(k[0]):
                kindMap[k[0]] = True
                holdingTypes += 1

    result["percentages"]= resDict
    result["totalInvested"] = round(totalVal, 2)
    result["holdingTypes"] = holdingTypes

    return network_response(result)


def stockTypes(request, acctIgnore=None):
    """
    STOCK TYPES MODULE:
    Returns the percentage at which the user's
    equity portion of their portfolio is split among
    different stock categories.

    OUTPUT:
    A JSON mapping 'securities', to a dictionary
    of category strings to their corresponding percentages,.
    {'securities': <Dictionary>,
     'types' : 4
     }
    """
    holds = request.user.profile.quovoUser.getDisplayHoldings(acctIgnore=acctIgnore)
    totalVal = sum([x.value for x in holds])
    # Compile a list of dictionaries, each of which associate the category of the equity
    # with its corresponding percentage towards the overall portfolio.
    breakDowns = [dict([(x.category, x.percentage * h.value/totalVal)
                for x in h.holding.equityBreakdowns.filter(updateIndex__exact=h.holding.currentUpdateIndex)])
                for h in holds]
    resDict = {'Materials': 0.0, 'Consumer Cyclic': 0.0, 'Financial': 0.0,
               'Real Estate': 0.0, 'Healthcare': 0.0, 'Utilities': 0.0,
               'Communication': 0.0, 'Energy': 0.0, 'Industrials': 0.0,
               'Technology': 0.0, 'Consumer Defense': 0.0, 'Services': 0.0,
               'Other': 0.0}
    # Keep totPercent as a normalizing constant
    # Compile all the percentages across our breakdowns
    # into the resDict.
    totPercent = 0
    for breakDown in breakDowns:
        for kind in resDict:
            if kind in breakDown:
                k = " ".join(re.findall('[A-Z][^A-Z]*', kind))
                resDict[k] += breakDown[kind]
                totPercent += breakDown[kind]
    # Make a few things prettier.
    resDict['Consumer'] = resDict.pop('Consumer Cyclic') + resDict.pop('Consumer Defense')
    resDict['Health Care'] = resDict.pop('Healthcare')
    if totPercent == 0:
        result = {}
        result['securities'] = {"None" : 100}
        result["types"] = 0
        return network_response(result)

    types = 0
    for kind in resDict:
        p = resDict[kind]/totPercent*100
        resDict[kind] = p
        if p >= 0.5:
            types += 1
    result = {}
    result['securities'] = resDict
    result["types"] = types
    return network_response(result)


def bondTypes(request, acctIgnore=None):
    """
    BOND TYPES MODULE:
    Returns the percentage at which the user's
    bond portion of their portfolio is split among
    different bond categories.

    OUTPUT:
    A JSON mapping 'securities', to a dictionary
    of category strings to their corresponding percentages..
    {'securities': <Dictionary>,
     'types' : 4
     }
    """
    holds = request.user.profile.quovoUser.getDisplayHoldings(acctIgnore=acctIgnore)
    totalVal = sum([x.value for x in holds])
    # Compile a list of dictionaries, each of which associate the category of the bond
    # with its corresponding percentage towards the overall portfolio.
    breakDowns = [dict([(x.category, x.percentage * h.value/totalVal)
                  for x in h.holding.bondBreakdowns.filter(updateIndex__exact=h.holding.currentUpdateIndex)])
                  for h in holds]
    resDict = {"Government": 0.0, "Municipal": 0.0, "Corporate": 0.0,
               "Securitized": 0.0, "Cash": 0.0, "Derivatives": 0.0}
    # Keep totPercent as a normalizing constant
    # Compile all the percentages across our breakdowns
    # into the resDict.
    totPercent = 0
    for breakDown in breakDowns:
        for kind in resDict:
            if kind in breakDown:
                resDict[kind] += breakDown[kind]
                totPercent += breakDown[kind]

    if totPercent == 0:
        result = {}
        result['securities'] = {"None": 100}
        result["types"] = 0
        return network_response(result)

    types = 0

    for kind in resDict:
        p = resDict[kind] / totPercent * 100
        resDict[kind] = p
        if p >= 0.5:
            types += 1
    result = {}
    result['securities'] = resDict
    result["types"] = types
    return network_response(result)


def contributionWithdraws(request, acctIgnore=None):
    """
    CONTRIBUTION / WITHDRAWALS MODULE:
    Returns the amount of money the user has invested/taken out
    of their account over the past four years, and the net amounts.

    OUTPUT:
    A JSON following the format  of the payload variable below.
    """
    qUser = request.user.profile.quovoUser
    withdraws = qUser.getWithdraws(acctIgnore=acctIgnore)
    contributions = qUser.getContributions(acctIgnore=acctIgnore)

    today = datetime.today()
    year = today.year
    oneYear = year
    twoYear = year - 1
    threeYear = year - 2

    payload = {
        "oneYear" : {
            "contributions": 0,
            "withdraw": 0,
            "net": 0
        },
        "twoYear" : {
            "contributions": 0,
            "withdraw": 0,
            "net": 0
        },
        "threeYear" : {
            "contributions": 0,
            "withdraw": 0,
            "net": 0
        },
        "total" : {
            "contributions": 0,
            "withdraw": 0,
            "net": 0
        }
    }

    def insert_payload(transaction, payload, category):
        date = transaction.date.year
        if date == oneYear:
            place = "oneYear"
        elif date == twoYear:
            place = "twoYear"
        elif date == threeYear:
            place = "threeYear"
        else:
            return
        payload[place][category] += abs(transaction.value)
        payload["total"][category] += abs(transaction.value)
        real_value = abs(transaction.value)
        if category == "withdraw":
            real_value = -real_value
        payload[place]["net"] += real_value
        payload["total"]["net"] += real_value

    for transaction in contributions:
        insert_payload(transaction, payload, "contributions")

    for transaction in withdraws:
        insert_payload(transaction, payload, "withdraw")

    return network_response(payload)


def returnsComparison(request, acctIgnore=None):
    qu = request.user.profile.quovoUser
    try:
        returns = qu.getUserReturns(acctIgnore=acctIgnore)
    except Exception:
        returns = {'yearToDate': 0.0, 'twoYearReturns': 0.0, 'oneYearReturns': 0.0}

    dispReturns = [round(returns['yearToDate'], 2), round(returns['oneYearReturns'], 2), round(returns['twoYearReturns'], 2)]

    ageGroup = ageMap(qu.userProfile.get_age())
    if ageGroup < 20: ageGroup = 20
    elif ageGroup > 80: ageGroup = 80
    try:
        avg = AverageUserReturns.objects.filter(ageGroup__exact=ageGroup).latest('createdAt')
    except AverageUserReturns.DoesNotExist:
        if AverageUserReturns.objects.exists():
            avg = AverageUserReturns.objects.filter(ageGroup__exact=0).latest('createdAt')
        else:
            avg = AverageUserReturns(yearToDate=0.0, oneYearReturns=0.0, twoYearReturns=0.0)
    avgUser = [round(avg.yearToDate, 2), round(avg.oneYearReturns, 2), round(avg.twoYearReturns, 2)]

    return network_response({
        "returns": dispReturns,
        "avgUser": avgUser,
        "ageGroup": str(ageGroup-4)+"-"+str(ageGroup)
    })


def riskAgeProfile(request, acctIgnore=None):
    profile = request.user.profile
    age = profile.get_age()
    birthyear = profile.birthday.year
    qu = profile.quovoUser
    if acctIgnore:
        userBondEq = qu.getUserBondEquity(acctIgnore=acctIgnore)
    else:
        userBondEq = qu.userBondEquity.latest('createdAt') if qu.userBondEquity.exists() else None

    bench = Benchmark.objects.annotate(abs_diff=Func(F('age_group') - age, function='ABS')).order_by('abs_diff').first()
    bench_bond_stock = bench.get_stock_bond_split()
    bench_stock_perc = bench_bond_stock.get("stock")
    bench_bond_perc = bench_bond_stock.get("bond")

    avgStock = 0
    avgBond = 0
    if AverageUserBondEquity.objects.exists():
        avgProf = AverageUserBondEquity.objects.latest('createdAt')
        avgStock = avgProf.equity
        avgBond = avgProf.bond

    stock_total = 0 if not userBondEq else userBondEq.equity
    bond_total = 0 if not userBondEq else userBondEq.bond

    a = ageMap(age)

    return network_response({
        "stock": int(round(stock_total)),
        "bond": int(round(bond_total)),
        "benchStock" : bench_stock_perc * 100,
        "benchBond" : bench_bond_perc * 100,
        "avgStock" : int(round(avgStock)),
        "avgBond" : int(round(avgBond)),
        "ageRange" : "%s-%s" % (a-4, a)
    })


def _compoundRets(B, r, n, k, cont):
    if np.isclose(r, 0):
        return B+cont*k
    result = max(B*(1+r/n)**(n*k) + cont/n*((1+r/n)**(n*k)-1)/(r/n)*(1+r/n), cont/n, 0)
    if math.isnan(result):
        return 0
    return result


def compInterest(request, acctIgnore=None):

    result = {
        "currentValue": 0,
        "yearsToRetirement": 0,
        "currentFees": 0,
        "averageAnnualReturns": 0,
        "futureValues": 0,
        "futureValuesMinusFees": 0,
        "netRealFutureValue": 0
    }
    quovo_user = request.user.profile.quovoUser
    holds = quovo_user.getDisplayHoldings(acctIgnore=acctIgnore)
    dispVal = sum([x.value for x in quovo_user.userCurrentHoldings.exclude(account__quovoID__in=acctIgnore)])

    if not holds: return network_response(result)
    valReach = 10

    weights = [x.value / dispVal for x in holds]
    feeList = []
    for h in holds:
        try:
            feeList.append(h.holding.expenseRatios.latest('createdAt').expense)
        except HoldingExpenseRatio.DoesNotExist:
            feeList.append(0.0)
    currFees = np.dot(weights, feeList)

    cont_with = json.loads(contributionWithdraws(request, acctIgnore=acctIgnore).content)
    avgCont = cont_with['data']['total']['net']/3.0

    avgAnnRets = np.dot(weights, [x.holding.returns.latest('createdAt').oneYearReturns for x in holds])
    futureValues = [round(_compoundRets(dispVal, avgAnnRets/100, 12, k, avgCont), 2) for k in range(0, valReach+1)]
    futureValuesMinusFees = [round(_compoundRets(dispVal, (avgAnnRets-currFees)/100, 12, k, avgCont), 2) for k in range(0, valReach+1)]
    netRealFutureValue = [round(_compoundRets(dispVal, (avgAnnRets-currFees-2)/100, 12, k, avgCont), 2) for k in range(0, valReach+1)]

    result["currentValue"] = dispVal
    result["yearsToRetirement"] = 10
    result["currentFees"] = currFees
    result["averageAnnualReturns"] = avgAnnRets
    result["futureValues"] = futureValues
    result["futureValuesMinusFees"] = futureValuesMinusFees
    result["netRealFutureValue"] = netRealFutureValue

    return network_response(result)


def portfolioHoldings(request, acctIgnore=None):
    result = {
        "holdings" : {}
    }
    qu = request.user.profile.quovoUser
    user_display_holdings = qu.userDisplayHoldings.exclude(holding__category__exact="IGNO").exclude(account__quovoID__in=acctIgnore)
    current_holdings = qu.getCurrentHoldings(acctIgnore=acctIgnore, exclude_holdings=[x.holding.id for x in user_display_holdings],
                                             showIgnore=True)
    total = sum(i.value for i in user_display_holdings) + sum(i.value for i in current_holdings)
    for user_display_holding in user_display_holdings:
        returns = user_display_holding.holding.returns.latest("createdAt")
        result["holdings"]["%s ( %s )" % (user_display_holding.holding.secname, user_display_holding.account.brokerage_name)] = {
            "isLink" : True,
            "value" : round(user_display_holding.value, 2),
            "portfolioPercent" : round(user_display_holding.value/total,2),
            "returns": round(returns.yearToDate, 2),
            "pastReturns" : round(returns.oneYearReturns, 2),
            "expenseRatio": round(user_display_holding.holding.expenseRatios.latest("createdAt").expense, 2),
        }

    for current_holding in current_holdings:
        result["holdings"][current_holding.holding.secname] = {
            "isLink" : False,
            "value" : round(current_holding.value, 2),
            "portfolioPercent" : round(current_holding.value/total, 2),
            "returns": None,
            "pastReturns": None,
            "expenseRatio": None,
        }

    return network_response(result)
