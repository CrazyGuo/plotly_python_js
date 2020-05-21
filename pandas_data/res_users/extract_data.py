# -*- coding: utf-8 -*-

import sys
import io
import os
import pandas as pd
import xlrd
 
dpath = os.getcwd() + '\\pandas_data\\res_users'

raw_file = dpath + '\\mps.xls'
xlrd_book = xlrd.open_workbook(raw_file, on_demand=True, formatting_info=True) 

df_batch = pd.read_excel(xlrd_book, sheet_name=0, header=0)

def format_group(group_name):
    g_list = str(group_name).split(',')
    ids = [ int(name) for name in g_list]
    result = [(6, False, ids)]
    return result

columns = df_batch.columns
for row in df_batch.itertuples(index=False):
    row_item = {}
    for index, col in enumerate(columns):
        if col == 'Groups/Name':
            row_item['groups_id'] = format_group(row[index])
        else:
            row_item[col.lower()] = row[index]
    print(row_item)
print(df_batch)