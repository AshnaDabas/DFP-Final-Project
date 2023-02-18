import tickerMapper as tm
import secDataPull as sec
from ticker_check import utility

if __name__ == "__main__":

    # Main loop continue until user enter 'quit'.

    stop = False
    while not stop:
        company = input("Please enter a company you would like to learn about(enter 'quit' to quit):")

        if company != 'quit' :
            util = utility()
            ticker = util.get_ticker(company)

            try:
                cik = tm.tickerToCIK(ticker)
                sec_data = sec.getSecData(cik)
                print(sec_data)

            except Exception as e: 
                print("Sorry, looks like we don't have any details on the company you provided at this time.")
                print(e)
        else:
            stop = True
    
    print("Thank you for using our sevices.")