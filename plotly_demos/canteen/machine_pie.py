
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
    result['total'] = result['bsum'] + result['lsum'] + result['dsum'] + result['msum']
    ser = pd.Series(result)
    return ser

#3.应用分组,被分组的字段是不存在mdf中的,会自动根据分组进行合并
result = data.groupby(['MachineNo']).apply(SumMachine)
result['MachineNo'] = result.index

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.3,
    specs=[ [{"type": "pie"}], [{"type": "table"}] ,
          ]
)

pie = go.Pie(labels=result['MachineNo'], values=result['total'])

fig.add_trace(pie, row= 1, col=1)

tb = go.Table(
    header=dict(values=list(result.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[result.bsum, result.lsum, result.dsum, result.msum, result.total, result.MachineNo],
               fill_color='lavender',
               align='left'))

fig.add_trace(tb, row= 2, col=1)

fig.update_layout(
    height=600,
    showlegend=True,
)  

fig.write_json(file="./plotlyjs/data.json")
