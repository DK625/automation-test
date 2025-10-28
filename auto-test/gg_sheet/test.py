import os 
import sys 

base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)

from constant.index import JSON_NAME
from utils.index import parse_sheet_to_object_purchase
from index import ConnectGoogleSheet

gg_sheet = ConnectGoogleSheet(JSON_NAME)
worksheet = gg_sheet.loadSheet_WorkSheet("1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY", "purchase_test_cases")
expectData, dataSheet = parse_sheet_to_object_purchase(worksheet)



print("=====================")
print (expectData)
print("=====================")
print(dataSheet)
print('=====================')
