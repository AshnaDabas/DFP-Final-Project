from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import streamlit as st

@st.cache_data
def get_nasdaq_current_stock_price(ticker):
    # tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOG", "GOOGL", "TSLA", "META", "AVGO", "PEP"]
    tickers = [ticker]
    websites = []
    prices = []
    times = []

    # for ticker in tickers:
    now = datetime.now()
    link = r"https://www.google.com/finance/quote/{}:NASDAQ".format(ticker)
    website = requests.get(link)
    soup = BeautifulSoup(website.content, 'html.parser')
    current_price = soup.find(class_ = "YMlKec fxKbKc") # Class that holds the current stock price
    current_price = str(current_price).split(">")[1].split("<")[0]
    print(ticker, current_price, now.date(), now.time())
    websites.append(link)
    prices.append(current_price)
    times.append(str(now.date()) + "\n" + str(now.time()))

    df = pd.DataFrame(list(zip(prices, times, websites)), index = tickers, columns = ['Current Price', 'Time of Price', 'URL'])

    return df

if __name__ == "__main__":
    get_nasdaq_current_stock_price("AAPL")