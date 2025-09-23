from array import array

# tools 
def parse_content(key, content):
    """
    Phân tích chuỗi content dựa vào key:
      - Nếu key là products/addresses => dict
      - Trong products, field 'items' sẽ thành list
      - providers => dict
      - list string 
      - string
    """
    if key in ('products', 'addresses'):
        parts = [p.strip() for p in content.split(',') if p.strip()]
        out = {}
        for p in parts:
            if ':' in p:
                k, v = p.split(':', 1)
                k = k.strip()
                v = v.strip()
                # nếu key là items => list
                if k == "items":
                    out.setdefault("items", []).append(v)
                else:
                    out[k] = v

        if 'city_index' in out:
            try:
                out['city_index'] = int(out['city_index'])
            except ValueError:
                pass
        return out

    if ':' in content and ',' in content:
        return {k.strip(): v.strip()
                for k, v in (item.split(':', 1)
                             for item in content.split(','))}

    if ',' in content and ':' not in content:
        return [x.strip() for x in content.split(',')]

    return content.strip()
def parse_string_to_array(string_input : str): 
    key, array = string_input.split(":")
    str_exclude_bracket = array.strip("[]")
    array_string = [f"{x.strip()}" for x in str_exclude_bracket.split(",")] # parse string to list ([])
    return (key, array_string)


def parse_column_expect_to_object(column_test_case ,column_field, column_data) : 
    result = {}
    len_sheet = len(column_test_case)
    is_processed = []
    data_locked = None # locked data
    is_locked_data = False # the variable to lock data 
    for i in range(len_sheet-1): 
        index = i + 1
        test_case = column_test_case[index]
        field  = column_field[index]
        data = data_locked if is_locked_data else column_data[index]
        is_locked_data = False # lock it , unlock when needed
        if test_case == "login": 
            if "login" not in is_processed : 
                result.setdefault("login", {})
                for part in data.split(",") :
                    k, v = part.split(":")
                    k = k.strip()
                    v = v.strip()
                    try : 
                        v = int(v)
                    except ValueError : 
                        pass
                    result["login"][k] = v 
                is_processed.append("login")
        elif test_case == "validate_empty_shipping_address_fields" : 
            if "validate_empty_shipping_address_fields" not in is_processed : 
                key,array = parse_string_to_array(data)
                result.setdefault("validate_empty_shipping_address_fields",{})
                result["validate_empty_shipping_address_fields"][key] = array
                is_processed.append("validate_empty_shipping_address_fields")
                data_locked = data 
                is_locked_data = True 
        else : 
            if "[" in data : 
                key,array = parse_string_to_array(data)
                result.setdefault(test_case,[])
                item = {}
                item.setdefault(field, {})
                item[field][key] = array
                result[test_case].append(item)
                continue
            else : 
                
                result.setdefault(test_case, [])
                item_data = {}
                item_data.setdefault(field, {})
                for part in data.split(","): 
                    if ":" in part : 
                        k, v = part.split(":")
                        k = k.strip()
                        v = v.strip()
                        try : 
                            v = int(v)
                        except ValueError : 
                            pass 
                        item_data[field][k] = v
                
                result[test_case].append(item_data)
    return result


# parser 
def parse_sheet_to_object_purchase(worksheet):
    """
    column A : test case 
    column B : field 
    column C : value 
    column D : expect
    column E : output
    column F : status 
    """

    col_A = worksheet.col_values(1)
    col_B = worksheet.col_values(2)
    col_C = worksheet.col_values(3)
    col_D = worksheet.col_values(4)

    dataExpect  = parse_column_expect_to_object(col_A, col_B, col_D)

    result = {}

    for i in range(len(col_A) - 1) : 
        index = i + 1 
        test_case = col_A[index]
        field = col_B[index]
        value = col_C[index]
        if test_case == "login" : 
            result.setdefault("login", {})
            result["login"].setdefault(field, [])

            if ("," in value):
                content = value.split(",")
                for sub in content : 
                    result["login"][field].append(sub.strip())

            else : 
                result["login"][field].append(value.strip())
            continue

        result.setdefault(test_case, {})
        result[test_case].setdefault(field, [])
        item_data = {}
        part_array = []
        for part in value.split(",") : 
            if ":" in part : 
                k, v = part.split(":")
                k = k.strip()
                v = v.strip()
                if k != "phone" : 
                    try:
                        v = int(v)
                    except ValueError:
                        pass

                item_data[k] = v
            else : 
                part_array.append(part)
                
        if (item_data): 
            result[test_case][field].append(item_data)
        else : 
            for part_t in part_array : 
                result[test_case][field].append(part_t)
    
    return ( dataExpect, result)
def parse_sheet_to_object_cart(worksheet) : 
    ''''
    In the Google Sheet : 
        Column A : test_case 
        Column B : field 
        Column C : value 
        Column D : expect 
    '''

    result = {}
    col_A = worksheet.col_values(1)
    col_B = worksheet.col_values(2)
    col_C = worksheet.col_values(3)
    col_D = worksheet.col_values(4)
    dataExpect = parse_column_expect_to_object(col_A, col_B, col_D)

    # len of columns must be equal 
    len_sheet = len(col_A)

    # pass element 0 (header)
    for i in range (len_sheet - 1): 
        index = i + 1
        test_case = col_A[index]
        field = col_B[index]
        value = col_C[index]

        if test_case == "login" : 
            result.setdefault("login", {})
            result["login"].setdefault(field, [])

            if ("," in value):
                content = value.split(",")
                for sub in content : 
                    result["login"][field].append(sub.strip())

            else : 
                result["login"][field].append(value.strip())
            continue

        item_data = {}
        item_data.setdefault(field, {})
        for part in value.split(",") : 
           
            if ":" in part : 
                k, v = part.split(":")
                k = k.strip()
                v = v.strip()
                try:
                        v = int(v)
                except ValueError:
                    pass

                item_data[field][k] = v
        result.setdefault(test_case, [])
        result[test_case].append(item_data)
    
    return ( dataExpect, result)


# write into gg sheet 
def log_to_sheet(sheet, test_name : str, status: str, details: str):
    """
    The sheet into GG Sheet following by : 
    column A : test case name 
    Column B : field 
    Column C : value
    Column D : expect 
    Column E : output
    Column F : status (PASSED || FAILED)
    """
    case_names = sheet.col_values(1)  # column A

    if test_name in case_names:
        row_index = case_names.index(test_name) + 1  # index return 0  ,
        sheet.update_cell(row_index, 5, details)  # column E = 5
        sheet.update_cell(row_index, 6, status)  # column F = 6
        
    else:
        # if not exist -> add new test case name 
        sheet.append_row([test_name,"","","", details, status])
def log_to_sheet_multi_rows(sheet, test_name : str, status: str, details_array : array[str], repeat_row : int):
    """
    The sheet into GG Sheet following by : 
    column A : test case name 
    Column B : field 
    Column C : value
    Column D : expect 
    Column E : output
    Column F : status (PASSED || FAILED)
    """
    case_names = sheet.col_values(1)  # column A

    if test_name in case_names:
        for i in range(repeat_row):
            row_index = case_names.index(test_name) + 1  # index return 0  ,
            sheet.update_cell(row_index + i, 5, details_array[i])  # column E = 5
            sheet.update_cell(row_index + i, 6, status)  # column F = 6
        
    else:
        # if not exist -> add new test case name 
        sheet.append_row([test_name,"","","", details_array[0], status]) # validate more closely 

def log_to_sheet_multi_rows_option(sheet, test_name : str, status: str, details_array : array[str], repeat_row_status : int, repeat_row_detail: int):
    """
    The sheet into GG Sheet following by : 
    column A : test case name 
    Column B : field 
    Column C : value
    Column D : expect 
    Column E : output
    Column F : status (PASSED || FAILED)
    """
    case_names = sheet.col_values(1)  # column A
    row_index = case_names.index(test_name) + 1 

    if test_name in case_names:
        if repeat_row_status : 
            for i in range(repeat_row_status):
                sheet.update_cell(row_index + i, 6, status)  # column F = 6
        if repeat_row_detail : 
            for i in range(repeat_row_detail): 
                sheet.update_cell(row_index + i, 5, details_array[i])  # column E = 5
        
        
    else:
        # if not exist -> add new test case name 
        sheet.append_row([test_name,"","","", details_array[0], status]) # validate more closely 
