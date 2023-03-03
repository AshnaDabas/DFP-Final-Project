import tickerMapper as tm
import secDataPull as sec
from ticker_check import ticker_check
import google_finance as google_finance
import yahooFinanceWebsite as yahoo_finance
import streamlit as st
from PIL import Image
import time
import pandas as pd


st.set_page_config(page_title="WealthSprout", page_icon=":seedling:", layout="wide")

#Header Layout
header_col, spacer = st.columns(2)
with header_col:
    header_col1, header_col2 = st.columns(2)
    with header_col1:
        logo = Image.open('./assets/wealthsprout.png')
        st.image(logo)

with st.spinner('Uploading Data...'):
    companies_df = pd.read_excel('ListOfCompanies.xlsx', sheet_name='Companies')
    selected_company = st.selectbox('Choose Company', companies_df, help='Select only one company to see financial details.')

#Search Bar
col_0, col_1 = st.columns((1,0.1))  
col_0.write('')
    
with st.spinner('Company list uploaded!'):
    time.sleep(1)

#Get Ticker
try:
    ticker_checker = ticker_check()
    ticker = ticker_checker.get_ticker(selected_company)
except Exception as e: 
    print("Sorry, looks like we don't have any details on the company you provided at this time.")
    print(e)

#Ticker display
ticker_col, spacer = st.columns(2)
with ticker_col:
    st.subheader(ticker)

#Content Layout - stock prices and ratio
spacer1, spacer2, spacer3 = st.columns(3)
spacer1, spacer2, spacer3 = st.columns(3)
current_price_col, ratio_col, spacer = st.columns(3)
try:
    google_finance_data = google_finance.get_nasdaq_current_stock_price(ticker)
    print(f"Current Price ({google_finance_data['Time of Price'].values[0][:10]})")
    print(google_finance.get_current_ratio(ticker))
    with current_price_col:
        current_price_col1, current_ratio_col2 = st.columns(2)
        with current_price_col1:
            st.markdown(f'<h3 title="Determined by the forces of supply and demand in the stock market">Current Price</h3>', unsafe_allow_html=True)
            st.subheader(google_finance_data["Current Price"].values[0])
        with ratio_col: 
            ratio_col1, ratio_col2 = st.columns(2)
            with ratio_col1:
                st.markdown(f'<h3 title="used to evaluate liquidity and their ability to meet its short-term obligations">Current Ratio</h3>', unsafe_allow_html=True)
                st.subheader(google_finance.get_current_ratio(ticker))
except Exception as e:
    with current_price_col:
        st.text("We are unable to find stock price information at this time")
    print(e)


#content layout - leadership and sec_filing
leadership_col, sec_filing_col = st.columns((.6, .4))  
try:
    yahoo_finance_data = yahoo_finance.getListOfCompanyExecutives(ticker)
    with leadership_col:
        st.text(f"Leadership at {selected_company}")
        st.write(yahoo_finance_data[['Name', 'Title']])
except Exception as e:
    with leadership_col:
        st.text("We are unable to find leadership information at this time")
    print(e)

try:
    cik = tm.tickerToCIK(ticker)
    sec_data = sec.getSecData(cik)
    sec_data['Filing Info'] = "CY " + sec_data['Year'] + " SEC 10-K"
    sec_display_data = sec_data.loc[:,["Filing Info", "Revenue (In Billions)", "Gross Profit Margin %", "Net Income (In Billions)", "Earnings Per Share (In Dollars)"]]
    sec_display_data["Year"] = sec_display_data["Filing Info"].str[3:8]
    with sec_filing_col:
        st.text(f"SEC Filing Information")
        st.text(f"Ticker: {ticker} Filing Name: {selected_company} CIK: {cik}")
        st.text("Obtained from SEC.gov - Link: SEC Filing Information")
        st.dataframe(sec_display_data[["Year", "Filing Info", "Gross Profit Margin %", "Earnings Per Share (In Dollars)"]])
except Exception as e:
    with sec_filing_col:
        st.text("We are unable to find filing details at this time")
    print(e)

#content layout - bar plot and company stats
col_spacer, col_spacer = st.columns(2)
col_spacer, col_spacer = st.columns(2)
bar_plot_col, spacer, stats_col = st.columns((.5, .1, .4))
try:
    cik = tm.tickerToCIK(ticker)
    sec_data = sec.getSecData(cik)
    sec_data['Filing Info'] = "CY " + sec_data['Year'] + " SEC 10-K"
    sec_display_data = sec_data.loc[:,["Filing Info", "Revenue (In Billions)", "Gross Profit Margin %", "Net Income (In Billions)", "Earnings Per Share (In Dollars)"]]
    sec_display_data["Year"] = sec_display_data["Filing Info"].str[3:8]

    with bar_plot_col:
        sec_plot_data = sec_display_data.loc[:,["Year", "Net Income (In Billions)", "Revenue (In Billions)"]]
        st.bar_chart(data=sec_plot_data, x="Year", use_container_width=True)
except Exception as e:
    with bar_plot_col:
        st.text("We are unable to find filing details at this time")
    print(e)

try:
    with stats_col:
        st.text('Company Statistics:')
        st.write(yahoo_finance.getCompanyStatistics(ticker))
except Exception as e:
    with stats_col:
        st.text("We are unable to find other company statistics at this time")
    print(e)

