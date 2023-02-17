#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Purpose: Pulls company SEC 10k filing information .json file and parses json for most recent 3 years of SEC filing information: revenue, gross profit margin (gross profit/revenue), net income, and earnings per share
Authors: Arthur Neumann
Requirements: urllib.request, json, datetime, pandas
Date: 02/16/2023

"""

import urllib.request
import json
import datetime
import numpy as np
import pandas as pd

ticker = ''
address = ''
header = ''


#Get current year and create string of current and previous 2 years
cYear = datetime.datetime.now().year
yearInt = [cYear-1, cYear-2, cYear-3]
yearStr = [str(cYear-1), str(cYear-2),str(cYear-3)]

#Set the address/header for JSON Retrieval from SEC using CIK
def setAddress(cik):
    global address
    global header
    address = 'https://data.sec.gov/api/xbrl/companyfacts/'+cik+'.json'
    header = {'User-Agent': 'Carnegie Mellon University aneumann@andrew.cmu.edu'}

#Get/load JSON from SEC
def getSecData(cik):
    setAddress(cik)
    req = urllib.request.Request(url=address, headers=header)
    res = urllib.request.urlopen(req)
    data = res.read()
    jData = json.loads(data)

    #Pull revenue information from within RevenueFromContractWithCustomerExcludingAssessedTax or Revenues entries, creating an empty list if no information available
    try:
        revenue = jData['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD']
    except:
        try:
            revenue = jData['facts']['us-gaap']['Revenues']['units']['USD']
        except:
            revenue = []
    
    #Parse revenue list and create a list of dictionaries with applicable values from each year if values are from most recent 3 years of 10k filings
    rIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in revenue if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not rIindex:
        rIindex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in revenue if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    #Parse list of dictionaries, convert string to float, and divide by 1 billion using each year's information as a key, creating an empty dictionary if no information available
    try:
        rVals = {line['year']: float(line['val']) / 1000000000 for line in rIindex}
    except:
        rVals = dict()
#Get/load JSON from SEC

    #Pull gross profit information from within 10-k GrossProfit entries and create a list of of dictionaries, creating an empty dictionary if no information available
    try:
        gross_profit = jData['facts']['us-gaap']['GrossProfit']['units']['USD']
        gpIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in gross_profit if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
        if not gpIndex:
            gpIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in gross_profit if
            entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]
        
        #Parse list of dictionaries, convert string to float, and divide by 1 billion, divide by revenue value and multiply by 100 using each year's information as a key, creating an empty dictionary if no information available
        gpVals = {line['year']: float(line['val'])/1000000000/rVals[line['year']]*100 for line in gpIndex}
    except:
        gpVals = dict()

    #Pull gross profit information from within 10-k GrossProfit entries and create a list of of dictionaries, creating an empty dictionary if no information available
    netIncome = jData['facts']['us-gaap']['NetIncomeLoss']['units']['USD']
    niIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in netIncome if
    entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not niIndex:
        niIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in netIncome if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    niVals = {line['year']: float(line['val']) / 1000000000 for line in niIndex}

    ePS = jData['facts']['us-gaap']['EarningsPerShareDiluted']['units']['USD/shares']
    epsIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in ePS if
        entry.get('form') == '10-K' and entry.get('end').startswith(yearStr[i]) and entry.get('frame') == ('CY'+yearStr[i])]
    if not epsIndex:
        epsIndex = [{'year': entry['frame'][-4:], 'val': entry['val']} for i in range(3) for entry in ePS if
        entry.get('form') == '10-K' and entry.get('end').startswith(str(int(yearStr[i]) + 1)) and entry.get('frame') == ('CY'+yearStr[i])]

    epsVals = {line['year']: float(line['val']) for line in epsIndex}

    years = list(rVals.keys())

    data = {
        'Year': years,
        'Revenue (In Billions)': [rVals[year] for year in years],
        'Gross Profit Margin %': [gpVals.get(year, '') for year in years],
        'Net Income (In Billions)': [niVals[year] for year in years],
        'Earnings Per Share (In Dollars)': [epsVals[year] for year in years],
        'SEC API Address': [address for year in years]
    }

    print(data)

    secDf = pd.DataFrame(data)
    secDf['Revenue (In Billions)'] = secDf['Revenue (In Billions)'].round(2)
    secDf['Gross Profit Margin %'] = secDf['Gross Profit Margin %'].replace('', np.nan)
    secDf['Gross Profit Margin %'] = secDf['Gross Profit Margin %'].round(2)
    secDf['Net Income (In Billions)'] = secDf['Net Income (In Billions)'].round(2)
    secDf['Earnings Per Share (In Dollars)'] = secDf['Earnings Per Share (In Dollars)'].round(2)

    return(secDf)

if __name__ == "__main__":
    import tickerMapper as tm
    print(getSecData(tm.tickerToCIK('AMZN')))