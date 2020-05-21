# -*- coding: utf-8 -*-
import os
import xlwt

dpath = os.getcwd() + '\\pandas_data\\format_excel'

raw_file = dpath + '\\test.xls'

wb = xlwt.Workbook()
# 添加一个表
ws = wb.add_sheet('sheet1')
# 3个参数分别为行号，列号，和内容
# 需要注意的是行号和列号都是从0开始的
ws.write(0, 0, '第1列')
ws.write(0, 1, '第2列')
ws.write(0, 2, '第3列')

# 保存excel文件
wb.save(raw_file)