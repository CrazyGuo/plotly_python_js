import plotly.graph_objects as go

import pandas as pd

colors = ['rgb(239, 243, 255)', 'rgb(189, 215, 231)', 'rgb(107, 174, 214)',
          'rgb(49, 130, 189)', 'rgb(8, 81, 156)']
data = {'Year' : [2010, 2011, 2012, 2013, 2014], 'Color' : colors}
df = pd.DataFrame(data)

fig = go.Figure(data=[go.Table(
  header=dict(
    values=["Color", "<b>YEAR</b>"],
    line_color='white', fill_color='white',
    align='center', font=dict(color='black', size=12)
  ),
  cells=dict(
    values=[df.Color, df.Year],
    line_color=[df.Color], fill_color=[df.Color],
    align='center', font=dict(color='black', size=11)
  ))
])

fig.write_json(file="./plotlyjs/data.json")


