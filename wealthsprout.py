import tickerMapper as tm
import secDataPull as sec
from ticker_check import utility
import google_finance as google_finance
import yahooFinanceWebsite as yahoo_finance
import stockChartsWebsite as stock_charts
import streamlit as st
import urllib.request
from PIL import Image

companies = ["Apple", "Microsoft", "Alphabet", "Amazon", "Tesla", "Meta", "NVIDIA", "PepsiCo", "Costco Wholesale",  "Broadcom"]
st.set_page_config(page_title="WealthSprout", page_icon=":seedling:", layout="wide")
selected_company = st.selectbox("Please select a company you would like to learn more about", companies)

util = utility()
print(f'getting data for {selected_company}')
ticker = util.get_ticker(selected_company)
print(ticker)
# company_filing_name = util.get_company_name(ticker)

try:
    cik = tm.tickerToCIK(ticker)
    print(cik)
    sec_data = sec.getSecData(cik)
    sec_data['Filing Info'] = "CY " + sec_data['Year'] + " SEC 10-K"
    sec_display_data = sec_data.loc[:,["Filing Info", "Revenue (In Billions)", "Gross Profit Margin %", "Net Income (In Billions)", "Earnings Per Share (In Dollars)"]]

    nasdaq_data = google_finance.get_nasdaq_current_stock_price(ticker)
    
    yahoo_finance_data = yahoo_finance.getListOfCompanyExecutives(ticker)
    
    print(sec_display_data)

except Exception as e: 
    print("Sorry, looks like we don't have any details on the company you provided at this time.")
    print(e)


st.write("SEC Filing Information")
st.write(f"Ticker: {ticker} Filing Name: {selected_company} CIK: {cik}")
st.write("Obtained from SEC.gov - Link: SEC Filing Information")
st.dataframe(sec_display_data)
st.write(nasdaq_data)
st.write(yahoo_finance_data)