
class ticker_check:
    ticker_company_mapping = {}
    
    def __init__(self) -> None:
        '''
        Function Description:
            Function initialization that reads in the NASDAQ.txt file
        Arguments:
            None
        Return Value:
            None, sets up the ticker_company mapping dictionary
        '''

        file_path = "assets/NASDAQ.txt"
        fin = open(file_path, 'rt', encoding='utf-8')
        for line in fin:
            words = line.split('\t')
            words.append(' ')
            self.ticker_company_mapping[words[1].replace('\n','').lower()] = words[0]
        fin.close()

    def get_ticker(self, company_name):
        '''
        Function Description:
            function to return company name
        Arguments:
            company_name: string for company name
        Return Value:
            ticker: string for company ticker
        '''
        company_name = company_name.lower()
        if company_name in self.ticker_company_mapping:
            return self.ticker_company_mapping[company_name]
        else:
            for key in self.ticker_company_mapping:
                if company_name in key:
                    return self.ticker_company_mapping[key]

if __name__ == "__main__":
    ticker_check = ticker_check()
    print(ticker_check.get_ticker('microsoft'))