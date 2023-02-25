#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from PIL import Image
from io import BytesIO
import shutil
import requests
from isort import stream
import streamlit as st

@st.cache_data
def getLinkToCompanyChart(stock_ticker):
    '''
    Function Description:
        Python program that pulls a link to the company chart from StockCharts website.
    Arguments:
        Stock Ticker as a string
    Return Value:
        A url to the company chart.
        Empty string if no stock ticker is passed, or if unable to get chart from website. 
    '''

    url_companyChart = ""
    
    # Pre-Condition
    if len(stock_ticker)==0: return url_companyChart
       
    # StockCharts website link
    url_website = 'https://stockcharts.com/h-sc/ui?s={}'.format(stock_ticker)
    
    try:
        req = Request(url_website, headers={'User-Agent': 'Mozilla/5.0'})

        html = urlopen(req)
    
        bs_website = BeautifulSoup(html.read(), "lxml")

        fout = open('bs_website_stockcharts.txt', 'wt', encoding='utf-8')
        fout.write(str(bs_website))
        fout.close()

        # Get a list of HTML tables on the web page
        table_list = bs_website.findAll('table')
        if len(table_list) == 0: return url_companyChart
        
        # Get the table fo key executive        
        img_list = bs_website.findAll('img')
        if len(img_list) == 0: return url_companyChart
        
        for img in img_list:
            try:
                #print(img['class'])
                if 'chartimg' in img['class']:
                    #print(img['src'])
                    url_companyChart = img['src']
                    url =  "https:"+url_companyChart
                    print(url)
                    
                    return url
            except Exception as e:  
                # Do nothing - Exceptions are expected because
                # not all images have a class
                print(e)
                pass 

    except:
        print("Exception: {}".format(sys.exc_info()))
        

# Testing
if __name__ == '__main__': 
    # Unit Test 1: Valid Stock Ticker
    url = getLinkToCompanyChart('AMZN')
    if len(url) == 0:
        print("Empty url")
    else:
        print(url)
    
    # Unit Test 2: No Stock Ticker
    url = getLinkToCompanyChart('')
    if len(url) == 0:
        print("Empty url")
    else:
        print(url)
    
    # Unit Test 3: Invalid Stock Ticker
    url = getLinkToCompanyChart('AMZN231')
    if len(url) == 0:
        print("Empty url")
    else:
        print(url)