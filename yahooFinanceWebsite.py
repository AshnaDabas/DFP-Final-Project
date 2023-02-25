#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request


def getListOfCompanyExecutives(stock_ticker):
    '''
    Function Description:
        Python program that pulls company's executives list from Yahoo Finance website.
    Arguments:
        Stock Ticker as a string
    Return Value:
        A DataFrame with a list of company executives along with their titles.
        None if an empty string is passed, or if the website retrurns no data. 
    '''
    
    # Pre-Condition
    if len(stock_ticker)==0: return
    
    # Yahoo Finace Page Link
    url_website = 'https://finance.yahoo.com/quote/{}/profile?p={}'.format(stock_ticker,stock_ticker)
    #print(url_website)
    
    try:
        req = Request(url_website, headers={'User-Agent': 'Mozilla/5.0'})

        html = urlopen(req)
    
        bs_website = BeautifulSoup(html.read(), "lxml")
        
        #fout = open('bs_website_company_profile.txt', 'wt', encoding='utf-8')
        #fout.write(str(bs_website))
        #fout.close()

        # Get a list of HTML tables on the web page
        table_list = bs_website.findAll('table')
        if len(table_list) == 0: return
        
        # Get the table fo key executive        
        table_key_executives = table_list[0]
        
        exec_list = []
        
        # Loop through the list of rows in the table. Each row represents an executive.              
        for row in table_key_executives.findAll('tr'):
            
            # Get list of columns in the row
            cols = row.findAll('td')

            # Skip through the first row / hearder row
            if len(cols) > 1:

                spans_name = cols[0].findAll('span')
                spans_title = cols[1].findAll('span')

                if len(spans_name) > 0 and len(spans_title) > 0:
                    exec_list.append([spans_name[0].string,spans_title[0].string])
                    #print('{}, {}'.format(spans_name[0].string, spans_title[0].string))
        
        # Convert list of lists to a dataframe
        exec_df = pd.DataFrame(exec_list, columns=['Name', 'Title'])
        return exec_df
        
    except:
        print("Exception: {}".format(sys.exc_info()))
        #pass


# Testing
if __name__ == '__main__':

    # Unit Test 1: Valid Stock Ticker
    df = getListOfCompanyExecutives('AMZN')
    print(df)
    
    # Unit Test 2: No Stock Ticker
    df = getListOfCompanyExecutives('')
    print(df)
    
    # Unit Test 3: Invalid Stock Ticker
    df = getListOfCompanyExecutives('AMZN231')
    print(df)