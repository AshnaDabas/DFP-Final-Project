
import urllib.request
import json
import tickerMapper
import datetime

ticker = ''
address = ''
header = ''

cYear = datetime.datetime.now().year
yearInt = [cYear-1, cYear-2, cYear-3]
yearStr = [str(cYear-1), str(cYear-2),str(cYear-3)]

def setTicker(iTicker):
    global ticker
    ticker = iTicker

def setAddress(cik):
    global address
    global header
    address = 'https://data.sec.gov/api/xbrl/companyfacts/'+cik+'.json'
    header = {'User-Agent': 'Carnegie Mellon University aneumann@andrew.cmu.edu'}

def getSecData(cik):
    setAddress(cik)
    req = urllib.request.Request(url=address, headers=header)
    res = urllib.request.urlopen(req)
    data = res.read()
    jData = json.loads(data)
    try:
        revenue = jData['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD']
    except:
        try:
            revenue = jData['facts']['us-gaap']['Revenues']['units']['USD']
        except:
            revenue = []
    rIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in revenue if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not rIindex:
        rIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in revenue if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    try:
        rVals = {line['year']: float(line['val']) / 1000000000 for line in rIindex}
    except:
        rVals = dict()

    try:
        gross_profit = jData['facts']['us-gaap']['GrossProfit']['units']['USD']
        gpIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in gross_profit if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
        if not gpIndex:
            gpIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in gross_profit if
            entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]
        
        gpVals = {line['year']: float(line['val'])/1000000000/rVals[line['year']]*100 for line in gpIndex}
    except:
        gpVals = dict()

    netIncome = jData['facts']['us-gaap']['NetIncomeLoss']['units']['USD']
    iIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in netIncome if
    entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not iIindex:
        iIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in netIncome if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    niVals = {line['year']: float(line['val']) / 1000000000 for line in iIindex}

    ePS = jData['facts']['us-gaap']['EarningsPerShareDiluted']['units']['USD/shares']
    epsIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in ePS if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not epsIndex:
        epsIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in ePS if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    epsVals = {line['year']: float(line['val']) for line in epsIndex}


    secDicts = [
        {'revenue': rVals},
        {'gross profit margin': gpVals},
        {'net income': niVals},
        {'earnings per share': epsVals}
    ]
    return(cik, address, secDicts)