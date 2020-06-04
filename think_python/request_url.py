# -*- coding: utf-8 -*-

import requests
import time
import datetime


url = 'https://wuzffalu.cn.flextronics.com/flexpsappapi/api/production/getplandata'
day_now = time.localtime()
daybegin = datetime.datetime.now() + datetime.timedelta(days=-30)
dayend = datetime.datetime.now() + datetime.timedelta(days=8)
params = {'start_date': '2020-04-03', 'end_date': '2020-04-04'}
try:
    request_result = requests.get(url, params=params).json()
except:
    request_result = None
data = []
print(request_result)
for item in request_result['Data']:
    it = item['Item']
    if it.startswith('ALCH-HB-3KC17938AAAR'):
        res = item['Item'].strip()
        result = "%s_%s_" % (res, item['Item'])
        print(result)
        im = {'item':item['Item']}
        print(im)