# -*- coding: utf-8 -*-

import requests

session_id = 'session_id=%s' % ('0d8c3eef107976266cd1eb8e735c7282795d6274')
headers = {'Content-Type': 'application/json', 'Cookie': session_id}

url = "http://127.0.0.1:8069/api/ionic/check_session"

params = { "params": { } }

r = requests.post(url, json=params, headers=headers)

print(r.text)