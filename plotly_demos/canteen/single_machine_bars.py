
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

fig = go.Figure(data=[
    go.Bar(name='Breakfast', x=result['ConsumeDate'], y=result['Breakfast']),
    go.Bar(name='Lunch', x=result['ConsumeDate'], y=result['Lunch']),
    go.Bar(name='Dinner', x=result['ConsumeDate'], y=result['Dinner']),
    go.Bar(name='MidnightSnack', x=result['ConsumeDate'], y=result['MidnightSnack']),
])

fig.write_json(file="./plotlyjs/data.json")
