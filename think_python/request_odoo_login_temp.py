# -*- coding: utf-8 -*-

import requests

'''
headers = {'Content-Type': 'application/json'}
url = "http://127.0.0.1:8069/api/ionic/login_auth"
params = { "params": {"login":"wuzhuguo", "pwd":"123456"} }


r = requests.post(url, json=params, headers=headers)

print(r.text)
'''

'''
headers = {'Content-Type': 'application/json', 'Cookie':'session_id=be44873a92b269ceb94a6259710fac2640b88a81'}
url = "http://127.0.0.1:8069/api/v2/wechat_apply_car"
params = { "params": 
                    {
                        "appliance_crew": 'Abc',
                        "reason": "Test", 
                        "depart_time": "2020-06-21 17:00:06", 
                        "depart_location": "苏州", 
                        "destination": "无锡",
                        "contact":"欢欢",
                        "contact_phone":"15862685371"
                    
        } }


r = requests.post(url, json=params, headers=headers)

print(r.text)
'''

headers = {'Content-Type': 'application/json', 'Cookie':'session_id=13a11ec910d7b2ac5d2be46e0520b2b5248150b0'}
url = "http://127.0.0.1:8069/api/v3/wechat_apply_car_approve"
params = { "params": 
                    {
                        "id": 1,
                        "status": "department_confirm", 
                        "remark": "Pass", 
                        "record_id": 1, 
                        "is_agree": True,
                    
        } }


r = requests.post(url, json=params, headers=headers)

print(r.text)