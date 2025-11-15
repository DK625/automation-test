from index import ConnectGoogleSheet

gg_sheet = ConnectGoogleSheet()
worksheet = gg_sheet.loadSheet_WorkSheet("1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY", "cart_test_cases")
dataSheet = worksheet.get_all_values()

print (dataSheet)