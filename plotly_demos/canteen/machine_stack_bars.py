
import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

#1.读取csv数据
dpath = os.getcwd() + '\\plotly_demos\\canteen'
raw_file = dpath + '\\canteen_data.csv'
data = pd.read_csv(raw_file, header=0)

#2.将数据按机器编号分组
def SumMachine(mdf):
    result = {
                'bsum' : mdf['Breakfast'].sum(),
                'lsum' : mdf['Lunch'].sum(),
                'dsum' : mdf['Dinner'].sum(),
                'msum' : mdf['MidnightSnack'].sum()
    }
    ser = pd.Series(result)
    return ser

#3.应用分组,被分组的字段是不存在mdf中的,会自动根据分组进行合并
result = data.groupby(['MachineNo']).apply(SumMachine)

fig = go.Figure(data=[
    go.Bar(name='Breakfast', x=result.index, y=result['bsum']),
    go.Bar(name='Lunch', x=result.index, y=result['lsum']),
    go.Bar(name='Dinner', x=result.index, y=result['dsum']),
    go.Bar(name='MidnightSnack', x=result.index, y=result['msum']),
])

fig.update_layout(barmode='stack')

fig.write_json(file="./plotlyjs/data.json")
