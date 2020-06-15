# -*- coding: utf-8 -*-

import requests

headers = {'Content-Type': 'application/json'}
url = "http://127.0.0.1:8069/api/ionic/login_auth"
params = { "params": {"login":"adm", "pwd":"adm123"} }


r = requests.post(url, json=params, headers=headers)

print(r.text)