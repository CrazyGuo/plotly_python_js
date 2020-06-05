
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
                'day_total' : mdf['Breakfast'] + mdf['Lunch'] + mdf['Dinner'] + mdf['MidnightSnack'],
                'date' : mdf['ConsumeDate'],
                'MachineNo':mdf['MachineNo']
    }
    ser = pd.DataFrame(result)
    return ser

#3.应用分组,被分组的字段是不存在mdf中的,会自动根据分组进行合并
result = data.groupby(['MachineNo']).apply(SumMachine)
print(result)
fig = px.line(result, x="date", y="day_total", color="MachineNo",line_group="MachineNo")


fig.write_json(file="./plotlyjs/data.json")
