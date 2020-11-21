
import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

#1.读取excel数据
dpath = os.getcwd() + '\\plotly_demos\\speech'
raw_file = dpath + '\\ah_counter.xlsx'
data = pd.read_excel(raw_file, header=0)

#2.将数据按目标名称分组
target_names = ['Ah', 'Um', 'Er', 'Well', 'So', 'Like', 'But', 'Repeats', 'Other']
def GroupNames(mdf):
    result = {   name: mdf[name].sum() for name in target_names }
    ser = pd.Series(result)
    return ser

#3.应用分组,被分组的字段是不存在mdf中的,会自动根据分组进行合并
result = data.groupby(['Name']).apply(GroupNames)

graph_data = [ go.Bar(name=n, x=result.index, y=result[n], text=result[n], textposition='auto') for n in target_names]

fig = go.Figure(data= graph_data)

fig.update_layout(barmode='stack')

fig.write_json(file="./plotlyjs/data.json")
