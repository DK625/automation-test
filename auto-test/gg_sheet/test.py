import os 
import sys 

base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)


from utils.index import parse_sheet_to_object_purchase
from index import ConnectGoogleSheet

gg_sheet = ConnectGoogleSheet("eminent-clover-471812-s3-80a07cb72b79.json")
worksheet = gg_sheet.loadSheet_WorkSheet("1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY", "purchase_test_cases")
expectData, dataSheet = parse_sheet_to_object_purchase(worksheet)



print("=====================")
print (expectData)
print("=====================")
print(dataSheet)
print('=====================')
