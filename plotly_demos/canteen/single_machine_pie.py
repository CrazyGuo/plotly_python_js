
import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

#1.读取csv数据
dpath = os.getcwd() + '\\plotly_demos\\canteen'
raw_file = dpath + '\\canteen_data.csv'
data = pd.read_csv(raw_file, header=0)


#2.筛选目标机器数据
result = data[data['MachineNo']=='SF0008']

count = len(result['Breakfast'])
name_val = ['Breakfast'] * count + ['Lunch'] * count + ['Dinner'] * count + ['MidnightSnack'] * count
name_serial = pd.Series(name_val)

val_serial = result['Breakfast'].copy()
val_serial = val_serial.append(result['Lunch'].copy())
val_serial = val_serial.append(result['Dinner'].copy())
val_serial = val_serial.append(result['MidnightSnack'].copy())

dict_data = {'name': name_serial.values, 'val': val_serial.values }
df = pd.DataFrame(dict_data)

pie = go.Pie(labels=df['name'], values=df['val'])
fig = go.Figure(pie)

fig.write_json(file="./plotlyjs/data.json")
