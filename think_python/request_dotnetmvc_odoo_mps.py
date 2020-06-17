# -*- coding: utf-8 -*-

import requests
import json

sid = None #
sid = 'e6cf329ed7725ae6b027223692180cd1581ffd3d'
headers = {'Content-Type': 'application/json', 'Cookie': "ab"}
net_url = "http://wuznt202/flexpsappapi/api/flexodoo/requestodoo"
odoo_url = "http://10.202.143.240:8070/api/ionic/login_auth"
odoo_params =  {'login': 'wuzhuguo', 'pwd':'Odoo@12345'} 

jons_string = json.dumps(odoo_params)

net_params = {"odoo_api": odoo_url, "odoo_params": jons_string}

if sid is None:
    request_result = requests.post(net_url, json=net_params, headers = headers).json()

    if request_result['IsSuccess'] and request_result['Data']:
        sid = request_result['Data']['result'].get("session", None)
        print(request_result)
else:
    session_id = 'session_id=%s' % (sid)
    headers['Cookie'] =  session_id
    print(session_id)
    odoo_url = "http://10.202.143.240:8070/api/mps/user_pending_list"
    odoo_params = {  "page_index": 1, "page_size": 10 }

    jons_string = json.dumps(odoo_params)
    net_params = {"odoo_api": odoo_url, "odoo_params": jons_string}

    mps_records = requests.post(net_url, json=net_params, headers=headers).json()
    print(mps_records)
