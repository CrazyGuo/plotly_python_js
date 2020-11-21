# -*- coding: utf-8 -*-
import os
import collections
import xlwt
import xlrd
import pandas as pd

dpath = os.getcwd() + '\\pandas_data\\flex_drawknife'
raw_file = dpath + '\\knife.xlsx'


xlrd_book = xlrd.open_workbook(raw_file, on_demand=True) 
df_batch = pd.read_excel(xlrd_book, sheet_name=1, header=0)

model_dic = collections.defaultdict(list)
for row in df_batch.itertuples(index=False):
    key = str(row[1]) +"_" + str(row[2])
    model_dic[key].append(row[0])

def format_name(name):
    parts = name.split('-')
    if len(parts) > 0:
        two_parts = parts[0].split('INCHV')
        if len(two_parts) == 2:
            return '_'.join(two_parts)
        else:
            return None
    else: 
        return None

result = collections.defaultdict(list)
df_batch2 = pd.read_excel(xlrd_book, sheet_name=0, header=0)
for row in df_batch2.itertuples(index=False):
    result['name'].append(row[0])
    result['location'].append(row[1])
    key = format_name(row[0])
    models = []
    if key:
        models.extend(model_dic[key])
        inches = key.split('_')
        result['dimension'].append(inches[0])
        result['Angle'].append(inches[1])
    result['models'].append(','.join(models))

pdout = pd.DataFrame(result)

pdout.to_excel(dpath + "\\output.xlsx") 

