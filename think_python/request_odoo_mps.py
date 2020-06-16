# -*- coding: utf-8 -*-

import requests

sid = 'f8a52dc534d6cfd2e4491a1a06532d8b4c064a65'
headers = {'Content-Type': 'application/json'}
url = "http://10.202.143.240:8070/api/ionic/login_auth"
params = { "params": {"login":"wuzhuguo", "pwd":"Odoo@12345"} }

if sid is None:
    request_result = requests.post(url, json=params, headers=headers).json()
    sid = request_result['result'].get("session", None)
    print(request_result)
else:
    session_id = 'session_id=%s' % (sid)
    headers['Cookie'] =  session_id

    url = "http://10.202.143.240:8070/api/mps/user_pending_list"
    params = { "params": { "page_index": 1, "page_size": 10} }

    mps_records = requests.post(url, json=params, headers=headers).json()
    print(mps_records)