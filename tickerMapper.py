#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Purpose: Pulls company name and SEC CIK key using NASDAQ Ticker from .csv file with ticker/SEC CIK for all companies
Authors: Arthur Neumann
Requirements: pip install sec_cik_mapper, os, csv
Date: 02/13/2023

"""

from sec_cik_mapper import StockMapper
from pathlib import Path
import os
import csv
import pandas as pd
import streamlit as st

#Assigning path and file name to path variable
cwd = os.getcwd()
csv_path = (cwd+"mutual_fund_mappings.csv")


mapper = StockMapper()
mapper.save_metadata_to_csv(csv_path)

with open(csv_path, 'r') as f:
    tickerMap = [row for row in csv.reader(f)]

tickerDf = pd.DataFrame(tickerMap[1:], columns=tickerMap[0])
tickerDf = tickerDf.loc[:, ['Ticker', 'Name', 'CIK', 'Exchange']]
tickerDf = tickerDf.set_index('Ticker')

@st.cache_data
def tickerToCompany(ticker):
    return tickerDf.loc[ticker,'Name']

@st.cache_data
def tickerToCIK(ticker):
    return 'CIK'+str(tickerDf.loc[ticker,'CIK'])
