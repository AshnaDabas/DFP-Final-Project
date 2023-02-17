import data_collection as dc
import data_standardization as ds
import data_transformation as dt
import json
import tickerMapper as tm
import secDataPull as sec
from ticker_check import utility

if __name__ == "__main__":
    company = input("Please enter a company you would like to learn about:")
    try:
        util = utility()
        ticker = util.get_ticker(company)
        cik = tm.tickerToCIK(ticker)
        print(sec.getSecData(cik))

    except Exception as e: 
        print("Sorry, looks like we don't have any details on the company you provided at this time."), print(e)

    
    

