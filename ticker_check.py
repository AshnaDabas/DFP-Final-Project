
class utility:
    ticker_company_mapping = {}
    
    def __init__(self) -> None:
        file_path = "assets/NASDAQ.txt"
        fin = open(file_path, 'rt', encoding='utf-8')
        for line in fin:
            words = line.split('\t')
            words.append(' ')
            self.ticker_company_mapping[words[1].replace('\n','').lower()] = words[0]

        # print(self.ticker_company_mapping)
        fin.close()


    def get_ticker(self, company_name):
        company_name = company_name.lower()
        if company_name in self.ticker_company_mapping:
            return self.ticker_company_mapping[company_name]
        else:
            for key in self.ticker_company_mapping:
                if company_name in key:
                    return self.ticker_company_mapping[key]

if __name__ == "__main__":
    util = utility()
    print(util.get_ticker('microsoft'))