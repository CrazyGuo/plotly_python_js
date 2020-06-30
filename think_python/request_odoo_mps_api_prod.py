# -*- coding: utf-8 -*-

import requests

'''
headers = {'Content-Type': 'application/json'}
url = "http://10.202.143.240:8070/api/ionic/login_auth"
params = { "params": {"login":"wuzhuguo", "pwd":"Odoo@12345"} }


r = requests.post(url, json=params, headers=headers)

print(r.text)

'''
'''
headers = {'Content-Type': 'application/json', 'Cookie':'session_id=e6cc557e2c68e94928da6d01e8cd31e146fe2ae0'}
url = "http://10.202.143.240:8070/api/mps/detail"
params = { "params": 
                    {
                        "id": 285
                    
        } }


r = requests.post(url, json=params, headers=headers)

print(r.text)
'''

headers = {'Content-Type': 'application/json', 'Cookie':'session_id=e6cc557e2c68e94928da6d01e8cd31e146fe2ae0'}
url = "http://10.202.143.240:8070/api/mps/user_pending_list"
params = { "params": 
                    {
                        "page_index": 1, "page_size": 10
                    
        } }


r = requests.post(url, json=params, headers=headers)

print(r.text)

