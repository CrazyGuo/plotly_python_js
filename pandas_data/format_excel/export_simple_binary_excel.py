# -*- coding: utf-8 -*-
import os
from io import BytesIO
import base64
import xlwt

wb = xlwt.Workbook()
# 添加一个表
ws = wb.add_sheet('sheet1')
# 3个参数分别为行号，列号，和内容
# 需要注意的是行号和列号都是从0开始的
ws.write(0, 0, '第1列')
ws.write(0, 1, '第2列')
ws.write(0, 2, '第3列')

fp = BytesIO()
wb.save(fp)
fp.seek(0)
content = fp.read()
fp.close()

content_base64 = base64.b64decode(content)
conetnt_len = len(content_base64)

print(conetnt_len)
