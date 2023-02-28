import tickerMapper as tm
import secDataPull as sec
import pandas as pd
from ticker_check import utility
import google_finance as google_finance
import yahooFinanceWebsite as yahoo_finance
import stockChartsWebsite as stock_charts
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import altair as alt


companies = ["Apple", "Microsoft", "Alphabet", "Amazon", "Tesla", "Meta Platforms", "NVIDIA", "PepsiCo", "Costco Wholesale",  "Broadcom"]
st.set_page_config(page_title="WealthSprout", page_icon=":seedling:", layout="wide")

#Header Layout
header_col1, header_col2 = st.columns(2)
with header_col1:
    header_col0_1, header_col0_2 = st.columns(2)
    with header_col0_1:
        logo = Image.open('./assets/wealthsprout.png')
        st.image(logo)

#Search Bar
col0, col2, col3 = st.columns(3)  
with col0:
    selected_company = st.selectbox("Please select a company you would like to learn more about", companies)

#Integration Logic
try:
    util = utility()
    ticker = util.get_ticker(selected_company)
    cik = tm.tickerToCIK(ticker)
    sec_data = sec.getSecData(cik)
    sec_data['Filing Info'] = "CY " + sec_data['Year'] + " SEC 10-K"
    sec_display_data = sec_data.loc[:,["Filing Info", "Revenue (In Billions)", "Gross Profit Margin %", "Net Income (In Billions)", "Earnings Per Share (In Dollars)"]]
    sec_display_data["Year"] = sec_display_data["Filing Info"].str[3:8]

    google_finance_data = google_finance.get_nasdaq_current_stock_price(ticker)

    google_finance_prices_dict = {"Price": [google_finance_data["Opening Price"], google_finance_data["Previous Closing Price"]],\
                                    "Type": ["O", "C"]}

    google_finance_prices_df = pd.DataFrame(google_finance_prices_dict)
    
    yahoo_finance_data = yahoo_finance.getListOfCompanyExecutives(ticker)
    
    # print(sec_display_data)

except Exception as e: 
    print("Sorry, looks like we don't have any details on the company you provided at this time.")
    print(e)

#ticker display
with col3:
    st.subheader(ticker)

#Content Layout - stock prices
spacer1, spacer2, spacer3 = st.columns(3)
col5, col6, col7 = st.columns(3)
try:
    with col5:
        col5_1, col5_2 = st.columns(2)
        with col5_1:
            st.text(f"Current Price ({google_finance_data['Time of Price'].values[0][:10]})")
            # st.text(f"As Of: {google_finance_data['Time of Price'].values[0][:10]}")
            st.subheader(google_finance_data["Current Price"].values[0])
        with col5_2:
            if google_finance_data["Opening Price"].values[0] > google_finance_data["Previous Closing Price"].values[0]:
                price_comparison = f'<p style="font-family:Courier; color:Green; font-size: 20px;">{google_finance_data["Previous Closing Price"].values[0]} &#8593</p>'
                st.markdown(price_comparison, unsafe_allow_html=True)
            else:
                price_comparison = f'<p style="font-family:Courier; color:Red; font-size: 20px;">{google_finance_data["Previous Closing Price"].values[0]} &#8595</p>'
                st.markdown(price_comparison, unsafe_allow_html=True)
except Exception as e:
    with col5:
        st.text("We are unable to find stock price information at this time")

# with col6:
#     col6_1, col6_2 = st.columns(2)
#     with col6_1:
#         st.text("Opening Price")
#         st.subheader(google_finance_data["Opening Price"].values[0])
#     with col6_2:
#         image = Image.open('./assets/fluctuation.png')
#         st.image(image, width = 100)

# with col7:
#     col7_1, col7_2 = st.columns(2)
#     with col7_1:
#         st.text("Previous Closing Price")
#         st.subheader(google_finance_data["Previous Closing Price"].values[0])
#     with col7_2:
#         image = Image.open('./assets/fluctuation.png')
#         st.image(image, width = 100)


#content layout - bar plot and filing details
col_spacer, col_spacer = st.columns(2)
col_spacer, col_spacer = st.columns(2)
col8, col9, col10 = st.columns((.5, .1, .4))

try:
    with col8:
        sec_plot_data = sec_display_data.loc[:,["Year", "Net Income (In Billions)", "Revenue (In Billions)"]]
        st.bar_chart(data=sec_plot_data, x="Year", use_container_width=True)

    with col10:
        st.text(f"SEC Filing Information")
        st.text(f"Ticker: {ticker} Filing Name: {selected_company} CIK: {cik}")
        st.text("Obtained from SEC.gov - Link: SEC Filing Information")
        st.dataframe(sec_display_data[["Year", "Filing Info", "Gross Profit Margin %", "Earnings Per Share (In Dollars)"]])
except Exception as e:
    with col8:
        st.text("We are unable to find filing details at this time")


#content layout - leadership
col10, col11 = st.columns(2)  
try:
    with col10:
        st.text(f"Leadership at {selected_company}")
        st.write(yahoo_finance_data[['Name', 'Title']])
except Exception as e:
    with col10:
        st.text("We are unable to find leadership information at this time")

#content layout - company statistics
try:
    with col11:
        st.text('Company Statistics:')
        st.write(yahoo_finance.getCompanyStatistics(ticker))
except Exception as e:
    with col11:
        st.text("We are unable to find other company statistics at this time")

#content layout - stock chart image
col12, col13 = st.columns(2)
try:
    with col12:
        company_chart = stock_charts.getCompanyChart(ticker)
        st.image(company_chart)
except Exception as e:
    with col12:
        st.text("We are unable to find stock charts at this time")

