# -*- coding: utf-8 -*-
import os
import xlwt

dpath = os.getcwd() + '\\pandas_data\\format_excel'

raw_file = dpath + '\\merge.xls'

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('My Sheet')
worksheet.write_merge(0, 0, 0, 3, 'First Merge') # Merges row 0's columns 0 through 3.
font = xlwt.Font() # Create Font
font.bold = True # Set font to Bold
style = xlwt.XFStyle() # Create Style
style.font = font # Add Bold Font to Style
# 合并Excel第2,3行,第1到第4列
worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style) 

# 保存excel文件
workbook.save(raw_file)