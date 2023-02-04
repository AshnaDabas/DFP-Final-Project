import data_collection as dc
import data_standardization as ds
import data_transformation as dt
import json


def setup_data():
    print("Reading all sources")
    input_source1 = dc.read_input_source1()
    input_source2 = dc.read_input_source2()
    input_source3 = dc.read_input_source3()

    print("Standardizing all sources")
    input_source_std1 = ds.cleanup_input_source1(input_source1)
    input_source_std2 = ds.cleanup_input_source2(input_source2)
    input_source_std3 = ds.cleanup_input_source3(input_source3)

    print("Reading companies list")
    company_file_path = "company_list.json"
    with open(company_file_path) as company_list_file:
        file_contents = company_list_file.read()
    company_list = json.loads(file_contents)['companies']
    print(company_list)

    print("Mapping data to companies")
    company_dict = dt.setup_company_data(company_list, input_source_std1, input_source_std2, input_source_std3)

    return company_dict

def display_company_data(company):
    print(f'displaying company data for company {company} ')
    

if __name__ == "__main__":
    company_dict = setup_data()
    company = input("Please enter a company you would like to learn about:")
    try:
        display_company_data(company_dict.get(company))
    except Exception as e: 
        print("Sorry, looks like we don't have any details on the company you provided at this time.")

    
    

