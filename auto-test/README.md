pytest cart_test_cases \ purchase_test_cases.py (cần active venv)

## Setup dự án ##

### cài các phụ thuộc (dependencies) ###
#### Di chuyển vào thư mục auto-test ####
- với python3 : 
```bash
python3 install -r requirements.txt
```
- với python : 
```bash
python install -r requirements.txt
```

### Khởi chạy môi trường ảo (venv) để chạy dự án 
```bash
source venv/bin/activate
```

### Chạy test ###
Có hai thư mục test là ```cart_test_cases``` và ```purchase_test_cases``` trong đó lần lượt có các file test là : 
- file ```cart_test_cases``` : tesst ESE luồng từ đăng nhập đến thêm vào giỏ hàng , kiểm trả giỏ hàng 

- file ```purchase_test_cases``` : test E2E luồng từ đăng nhập đến đặt hàng 

#### Di chuyển vào trong thư mục muốn test : ####
- Dùng câu lệnh ```pytest``` với file .py tương ứng , vd : 
```bash
   pytest purchase_test.cases.py
```
- Chạy với chế độ debug : 
   ``` bash
   pytest -s purchase_test_cases.py --pdb
   ```
  - ```--pdb``` : không đóng trình duyệt đang test khi có bug 
  - ``` -s ``` : mặc định pytest chặn luồng đầu ra có nghĩa là các dòng trong print sẽ không hiển thị ra terminal , tùy chọn này giúp khắc phục điều này , hiển thị ra terminal 

### Format của dữ liệu lấy về từ Google Sheet ###
#### purchase test case file ####
```python
# expectData : dữ liệu mong đợi của test case
expectData = {
   "login":{
      "failed":"Email hoặc mật khẩu không chính xác",
      "success":"Đăng nhập thành công"
   },
   "validate_empty_shipping_address_fields":{
      "error":[
         "Trường này bắt buộc",
         "Trường này bắt buộc",
         "The phone number is min 9 number"
      ]
   },
   "test_multiple_addresses":[
      {
         "addresses":{
            "full_address":"John Doe 0971234567 123 Chill Street Hà Nội"
         }
      },
      {
         "addresses":{
            "full_address":"John Doe 0971234567 123 Test Street Hà Nội"
         }
      },
      {
         "addresses":{
            "full_address":"John Doe 0971234567 123 Meo Street Hà Nội"
         }
      }
   ],
   "test_shipping_fee":[
      {
         "providers":{
            "shopee":"20.000 VND",
            "ghtk":"1.000 VND"
         }
      }
   ],
   "test_price_calculation":[
      {
         "product_prices":{
            "content":[
               "527.000 VND",
               "9.500.000 VND",
               "1.689.000 VND",
               "890.000 VND",
               "228.810 VND"
            ]
         }
      }
   ],
   "test_update_delivery_address_and_verify_display":[
      {
         "delivery_address":{
            "content":"John Doe 0971234567 123 Test Street Hà Nội"
         }
      }
   ],
   "test_cart_to_purchase_flow_integration":[
      {
         "quantity":{
            "content":0
         }
      }
   ],
   "TEST TEAR DOWN":[
      {
         "null":{
            
         }
      }
   ]
}
#==================================
# dataSheet : đầu vào của test case
dataSheet = {
   "login":{
      "username":[
         "example@gmail.com"
      ],
      "password":[
         "123456@Examplezzz", # wrong password
         "123456@Example" # correct password
      ]
   },
   "validate_empty_shipping_address_fields":{
      "products":[
         {
            "tab":"Làm Đẹp",
            "items":"Eyeshadow Palette with Mirror"
         },
         {
            "tab":"Đồ Dùng Gia Đình",
            "items":"Điều hòa"
         },
         {
            "tab":"Đồ Điện Tử",
            "items":"WD 2TB Elements Portable External Hard Drive - USB 3.0"
         },
         {
            "tab":"Phụ Kiện",
            "items":"Tai nghe Bluetooth"
         },
         {
            "tab":"Trang Sức",
            "items":"White Gold Plated Princess"
         }
      ]
   },
   "test_multiple_addresses":{
      "addresses":[
         {
            "name":"John Doe",
            "address":"123 Chill Street",
            "phone":"0971234567",
            "city_index":0
         },
         {
            "name":"John Doe",
            "address":"123 Test Street",
            "phone":"0971234567",
            "city_index":0
         },
         {
            "name":"John Doe",
            "address":"123 Meo Street",
            "phone":"0971234567",
            "city_index":0
         }
      ]
   },
   "test_shipping_fee":{
      "providers":[
         "null"
      ]
   },
   "test_price_calculation":{
      "product_prices":[
         "null"
      ]
   },
   "test_update_delivery_address_and_verify_display":{
      "delivery_address":[
         "null"
      ]
   },
   "test_cart_to_purchase_flow_integration":{
      "quantity":[
         "null"
      ]
   },
   "TEST TEAR DOWN":{
      "null":[
         "null"
      ]
   }
}
```

#### cart test case file ####
```python
# expectData : dữ liệu mong đợi của test case
expectData = {
   "login":{
      "failed":"Email hoặc mật khẩu không chính xác",
      "success":"Đăng nhập thành công"
   },
   "add_to_cart":[
      {
         "Tai nghe Bluetooth":{
            "name":"Tai nghe Bluetooth",
            "quantity":1,
            "price":"801.000 VND"
         }
      },
      {
         "Ốp lưng điện thoại":{
            "name":"Ốp lưng điện thoại",
            "quantity":1,
            "price":"378.000 VND"
         }
      },
      {
         "Đồng hồ thông minh":{
            "name":"Đồng hồ thông minh",
            "quantity":1,
            "price":"2.880.000 VND"
         }
      }
   ],
   "increase_decrease_quantity":[
      {
         "Tai nghe Bluetooth":{
            "initial_quantity":1,
            "total_after_increase":11,
            "total_after_decrease":9
         }
      },
      {
         "Ốp lưng điện thoại":{
            "initial_quantity":1,
            "total_after_increase":6,
            "total_after_decrease":5
         }
      },
      {
         "Đồng hồ thông minh":{
            "initial_quantity":1,
            "total_after_increase":4,
            "total_after_decrease":4
         }
      }
   ],
   "cart_total_amount_calculation":[
      {
         "Tai nghe Bluetooth":{
            "initial_quantity":9,
            "total_price":7209000
         }
      },
      {
         "Ốp lưng điện thoại":{
            "initial_quantity":5,
            "total_price":1890000
         }
      },
      {
         "Đồng hồ thông minh":{
            "initial_quantity":4,
            "total_price":1890000
         }
      }
   ],
   "delete_product":[
      {
         "Tai nghe Bluetooth":{
            "quantity":0
         }
      },
      {
         "Ốp lưng điện thoại":{
            "quantity":0
         }
      },
      {
         "Đồng hồ thông minh":{
            "quantity":0
         }
      }
   ]
}

# ================
# dataSheet : đầu vào của test case
dataSheet = {
   "login":{
      "username":[
         "example@gmail.com"
      ],
      "password":[
         "123456@Examplezzz", # wrong password
         "123456@Example" # correct password
      ]
   },
   "add_to_cart":{
      "Tai nghe Bluetooth":[
         {
            "quantity":1
         }
      ],
      "Ốp lưng điện thoại":[
         {
            "quantity":1
         }
      ],
      "Đồng hồ thông minh":[
         {
            "quantity":1
         }
      ]
   },
   "increase_decrease_quantity":{
      "Tai nghe Bluetooth":[
         {
            "increase_quantity":10,
            "decrease_quantity":2
         }
      ],
      "Ốp lưng điện thoại":[
         {
            "increase_quantity":5,
            "decrease_quantity":1
         }
      ],
      "Đồng hồ thông minh":[
         {
            "increase_quantity":3,
            "decrease_quantity":0
         }
      ]
   },
   "cart_total_amount_calculation":{
      "Tai nghe Bluetooth":[
         ""
      ],
      "Ốp lưng điện thoại":[
         ""
      ],
      "Đồng hồ thông minh":[
         ""
      ]
   },
   "delete_product":{
      "Tai nghe Bluetooth":[
         {
            "initial_quantity":9
         }
      ],
      "Ốp lưng điện thoại":[
         {
            "initial_quantity":5
         }
      ],
      "Đồng hồ thông minh":[
         {
            "initial_quantity":4
         }
      ]
   }
}
```

```JSON_NAME``` trong ***constants*** folder là tên ***file (credential)*** để kết nối đến google sheet api, trong thư mục gg_sheet cũng dán vào file key này để kết nối đến google sheet 

Điền các trường trong gg sheet theo đúng mẫu dược sheet (để ý kể cả khoảng trắng)

link sheet : https://docs.google.com/spreadsheets/d/1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY/edit?usp=sharing
