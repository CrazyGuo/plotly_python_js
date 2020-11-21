# -*- coding: utf-8 -*-

import requests
import json

sid = None #
#sid = 'e6cc557e2c68e94928da6d01e8cd31e146fe2ae0'
headers = {'Content-Type': 'application/json', 'Cookie': "ad"}
net_url = "https://asicweb.flex.com/empsapi_wuz/api/flexodoo/requestodoo"

net_url = "https://wuznte801.asia.ad.flextronics.com/empsapi2/api/flexodoo/requestodoo"
#net_url = "https://wuzffalu.cn.flextronics.com/empsapi2/api/flexodoo/requestodoo"
odoo_url = "http://10.202.143.240:8070/api/ionic/login_auth"
odoo_params =  {'login': 'wuzhuguo', 'pwd':'leetcode@123', } 

jons_string = json.dumps(odoo_params)

net_params = {"odoo_api": odoo_url, "odoo_params": jons_string, "session_id":""}

if sid is None:
    request_result = requests.post(net_url, json=net_params, headers = headers)
    print(request_result.text)

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
