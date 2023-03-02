#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import streamlit as st


def getCompanyChart(stock_ticker):
    '''
    Function Description:
        Python program that pulls an image og the company chart from StockCharts website.
    Arguments:
        Stock Ticker as a string
    Return Value:
        A png value of the company chart.
        None if no stock ticker is passed, or if unable to get chart from website. 
    '''

    
    url_website = 'https://stockcharts.com/h-sc/ui?s={}'.format(stock_ticker)

    options = Options()
    options.headless = True

    browsers = [webdriver.Firefox, webdriver.Chrome, webdriver.Edge, webdriver.Safari]

    for browser in browsers:
        try:
            driver = browser(options=options)
            break
        except:
            print(f'Can not control browser {str(browser)}')


    driver.get(url_website)

    # Close ads if present
    try:
        close_button = driver.find_element(By.CLASS_NAME, "fs-close-button")
        close_button.click()
    except :
        print("Exception: {}".format(sys.exc_info()))
        print('No ads')


    # Screenshot the chart
    try:
        stock_chart = driver.find_element(By.CLASS_NAME, "chartimg").screenshot_as_png
    except:
        print("Exception: {}".format(sys.exc_info()))
        print('Can not find img')
        stock_chart = None

    driver.quit()
    
    return stock_chart
        

# Testing
if __name__ == '__main__': 
    # Unit Test 1: Valid Stock Ticker
    img = getCompanyChart('AMZN')
    if img == None:
        print("Empty url")
    else:
        st.image(img)
    
    # Unit Test 2: No Stock Ticker
    img = getCompanyChart('')
    if img == None:
        print("Empty url")
    else:
        st.image(img)
    
    # Unit Test 3: Invalid Stock Ticker
    img = getCompanyChart('AMZN231')
    if img == None:
        print("Empty url")
    else:
        st.image(img)