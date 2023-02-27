from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd


def get_nasdaq_current_stock_price(ticker):
    tickers = [ticker]
    websites = []
    prices = []
    p_prices = []
    opens = []
    times = []

        # Start by getting current date and time
    now = datetime.now()
    
    # Create a link to Google Finance for the respective "ticker" and load into bs4 format
    link = r"https://www.google.com/finance/quote/{}:NASDAQ".format(ticker)
    website = requests.get(link)
    soup = BeautifulSoup(website.content, 'html.parser')
    
    # Find the HTML tag for the current price
    current_price = str(soup.find(class_ = "YMlKec fxKbKc")).split(">")[1].split("<")[0]
    
    # All other pertinent prices are listed under the same class name, let's find all of them
    all_price = soup.find_all(class_ = "P6K39c")
    
    # Previous close is the first
    previous_close = str(all_price[0]).split(">")[1].split("<")[0] # Class holding the previous close
    
    # Opening price is found in the day range, as the first value
    open_price = str(all_price[1]).split(">")[1].split("<")[0].split(" ")[0]
    
    # Print results for QA purposes
    print(ticker, current_price, previous_close, open_price, now.date(), now.time())
    
    # Append values to their respective lists
    websites.append(link)
    prices.append(current_price)
    p_prices.append(previous_close)
    opens.append(open_price)
    times.append(str(now.date()) + " - " + str(now.time()))

    # Create DF to house all data, with stock ticker as the index
    df = pd.DataFrame(list(zip(prices, p_prices, opens, times, websites)), index = tickers, columns = ['Current Price', "Previous Closing Price", "Opening Price", 'Time of Price', 'URL'])
    return df

if __name__ == "__main__":
    df = get_nasdaq_current_stock_price("AMZN")
    print(df)