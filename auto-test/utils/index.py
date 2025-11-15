

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


def parseSheetToObjectPurchase(rows):
    result = {}
    for section, child, content in rows[1:]:  # bỏ header
        val = parse_content(child, content)

        if section not in result:
            result[section] = {}

        # login đặc biệt: value phải là list
        if section == 'login':
            result[section].setdefault(child, [])
            result[section][child].append(val)
            continue

        # products / addresses => list các dict
        if child in ('products', 'addresses'):
            result[section].setdefault(child, [])
            result[section][child].append(val)
            continue

        result[section][child] = val

    return result


def parseSheetToObjectCart(rows):
    result = {}

    for section, child, content in rows[1:]:  
        if section == "login":
            result.setdefault("login", {})
            result["login"].setdefault(child, [])
            result["login"][child].append(content.strip())
            continue

        if section == "add_to_cart":
           
            item_data = {}
            for part in content.split(","):
                if ":" in part:
                    k, v = part.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    try:
                        v = int(v)
                    except ValueError:
                        pass
                    item_data[k] = v

            result.setdefault("add_to_cart", [])
            result["add_to_cart"].append({child: item_data})

    return result


