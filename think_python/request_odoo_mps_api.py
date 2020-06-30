# -*- coding: utf-8 -*-

import requests

'''
headers = {'Content-Type': 'application/json'}
url = "http://127.0.0.1:8069/api/ionic/login_auth"
params = { "params": {"login":"wuzhuguo", "pwd":"123456"} }


r = requests.post(url, json=params, headers=headers)

print(r.text)
'''
user_list = [1,2,3]
user_id = 1
if user_id in user_list:
    print("here")

headers = {'Content-Type': 'application/json', 'Cookie':'session_id=87f2b075951587744381020f1ab21de992b50f3b'}
url = "http://127.0.0.1:8069/api/mps/detail"
params = { "params": 
                    {
                        "id": 3
                    
        } }


r = requests.post(url, json=params, headers=headers)

print(r.text)
