from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st

stock_ticker = 'AMZN'
url_website = 'https://stockcharts.com/h-sc/ui?s={}'.format(stock_ticker)

driver = webdriver.Firefox()
driver.get(url_website)

try:
    close_button = driver.find_element(By.CLASS_NAME, "fs-close-button")
    close_button.click()
except:
    pass

stock_chart = driver.find_element(By.CLASS_NAME, "chartimg").screenshot_as_png
driver.close()

st.image(stock_chart)