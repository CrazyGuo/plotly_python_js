
import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

#1.读取csv数据
dpath = os.getcwd() + '\\line_plotly'
raw_file = dpath + '\\temperature.csv'
data = pd.read_csv(raw_file, header=0)

#2.将数据分成2大部分
#part1_data = data[data['refrigerator'] <= 7 ]
#part2_data = data[data['refrigerator'] > 7 ]

count = 8
#3.构造图形
fig = make_subplots(
    rows=count, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[ [{"type": "scatter"}], [{"type": "scatter"}] ,[{"type": "scatter"}] ,[{"type": "scatter"}] , 
            [{"type": "scatter"}] ,[{"type": "scatter"}] ,[{"type": "scatter"}] ,[{"type": "scatter"}]
          ]
)
for i in range(count):
    refrigerator_number = i + 1
    temp_data = data[data['refrigerator'] == refrigerator_number ]
    fig.add_trace(
        go.Scatter(
            x=temp_data["Datetime"],
            y=temp_data["temperature"],
            mode="lines",
            name="Refrigerator%d" % (refrigerator_number)
        ),
        row=refrigerator_number, 
        col=1
    )

fig.update_layout(
    height=1200,
    showlegend=True,
    title_text="Bitcoin",
)    

fig.write_json(file="./plotlyjs/data.json")
