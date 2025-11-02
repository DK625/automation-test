import os 
import sys 

base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)

from constant.index import JSON_NAME, SPREEDSHEET_ID
from utils.index import parse_sheet_to_object_purchase
from index import ConnectGoogleSheet

gg_sheet = ConnectGoogleSheet(JSON_NAME)
worksheet = gg_sheet.loadSheet_WorkSheet(SPREEDSHEET_ID, "purchase_test_cases")
expectData, dataSheet = parse_sheet_to_object_purchase(worksheet)



print("=====================")
print (expectData)
print("=====================")
print(dataSheet)
print('=====================')
