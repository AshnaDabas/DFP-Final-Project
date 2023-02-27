#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request

def getCompanyStatistics(stock_ticker):
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
    url_website = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(stock_ticker,stock_ticker)
    #print(url_website)
    
    try:
        # make a http request call to the yahoo finace website 
        req = Request(url_website, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        # load response data to Beautiful Soup
        bs_website = BeautifulSoup(html.read(), "lxml")
        
        #fname = 'bs_website_company_statistics.txt'
        #fout = open(fname, 'wt', encoding='utf-8')
        #fout.write(str(bs_website))
        #fout.close()
        #with open(fname, 'r') as f:
        #    page = f.read()
        #    f.close()

        # Get a list of HTML tables on the web page
        table_list = bs_website.findAll('table')

        # quick check to see if expected table is returned
        if len(table_list) == 0: return
        
        # The first tale has the financial statistics we seek
        table_company_statistics = table_list[0]
        
        # declare & instantiate variables
        dict_stats = {}
        valuation_measures = []
        raw_data = []
        header = []
        
        # loop through the table to extract statistics header and data
        for i, row in enumerate(table_company_statistics.findAll('tr')):

            # The row has the header info  
            if i == 0:
        
                #loop through the header information
                for j, col in enumerate(row.findAll('th')):
                    
                    # Simplify the header text for this specific column. The rest col header text are Ok.
                    if j == 1:
                        header = ['Current']
                    else:
                        header.append(col.text)

            else:
                
                fin_data = []
                
                #loop through the statistics label and data
                for j, col in enumerate(row.findAll('td')):
                    
                    # the first column is the label
                    if j == 0:
                        valuation_measures.append(col.text.strip())
                        label = col.text
                    else:
                        fin_data.append(col.text)
                
                # add to a dict
                dict_stats[label] = fin_data
                raw_data.append(fin_data)

        # convert to a dataframe                
        df_statistics = pd.DataFrame(raw_data, columns=header, index = valuation_measures)

        # return dataframe
        return df_statistics
        
    except:
        print("Exception: {}".format(sys.exc_info()))
        #pass



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
    df = getCompanyStatistics('AMZN')
    print(df)
    
    # Unit Test 2: No Stock Ticker
    df = getCompanyStatistics('')
    print(df)
    
    # Unit Test 3: Invalid Stock Ticker
    df = getCompanyStatistics('AMZN231')
    print(df)
    
    # Unit Test 1: Valid Stock Ticker
    df = getListOfCompanyExecutives('AMZN')
    print(df)
    
    # Unit Test 2: No Stock Ticker
    df = getListOfCompanyExecutives('')
    print(df)
    
    # Unit Test 3: Invalid Stock Ticker
    df = getListOfCompanyExecutives('AMZN231')
    print(df)
    