from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

# Setup necessary lists
tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOG", "GOOGL", "TSLA", "META", "AVGO", "PEP"]
websites = []
prices = []
p_prices = []
opens = []
pes = []
times = []

def get_nasdaq_current_stock_price(ticker):
    # Setup necessary lists
    tickers = [ticker]
    websites = []
    prices = []
    p_prices = []
    opens = []
    pes = []
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

    # Day range prices are found in the second
    open_price = str(all_price[1]).split(">")[1].split("<")[0]

    # P/E Ratio is the 6th
    pe = str(all_price[5]).split(">")[1].split("<")[0]

    # Print results for QA purposes
    # print(ticker, current_price, previous_close, open_price, now.date(), now.time())

    # Append values to their respective lists
    websites.append(link)
    prices.append(current_price)
    p_prices.append(previous_close)
    opens.append(open_price)
    times.append(str(now.date()) + " - " + str(now.time()))
    pes.append(pe)

    # Find absolute and relative differences between current price and yesterday's close
    absolutes = ["$" + str(round(float(i[1:]) - float(j[1:]), 2)) for i, j in zip(prices, p_prices)]
    relatives = [str(round((float(i[1:]) - float(j[1:])) / float(j[1:]) * 100, 2)) + "%" for i, j in zip(prices, p_prices)]

    # Create DF to house all data, with stock ticker as the index
    df = pd.DataFrame(list(zip(prices, p_prices, opens, absolutes, relatives, pes, times, websites)), index = tickers, columns = ['Current Price', "Previous Closing Price", "Day Range", "Absolute Price Change", "Percent Price Change", "P/E", 'Time of Price', 'URL'])
    return df


def get_current_ratio(ticker):
    # Create a link to Google Finance for the respective "ticker" and load into bs4 format
    link = r"https://www.google.com/finance/quote/{}:NASDAQ".format(ticker)
    website = requests.get(link)
    soup = BeautifulSoup(website.content, 'html.parser')

    bsheet_table = soup.find_all(name='table')[1]
    bsheet_cells = bsheet_table.find_all(name='td')

    final_cells = []
    for index in range(len(bsheet_cells)):
        if index % 3 == 0:
            for div in bsheet_cells[index].find_all(name='div'):
                final_cells.append(div.text)
        else:
            final_cells.append(bsheet_cells[index].text)

    final_table = list(zip(*[iter(final_cells)]*4))

    try:
        current_ratio = round(float(final_table[1][2].replace('B', '')) / float(final_table[2][2].replace('B', '')),2)
    except:
        current_ratio = '-'

    return current_ratio



if __name__ == "__main__":
    df = get_nasdaq_current_stock_price("AMZN")
    print(df)

    cr = get_current_ratio('AMZN')
    print(cr)
