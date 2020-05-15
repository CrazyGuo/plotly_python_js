import plotly.graph_objects as go

headers = dict(values=['A Scores', 'B Scores'])
cells = dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]])
table = go.Table(header = headers, cells = cells)

fig = go.Figure(data=[table])
#获取json格式 供前端使用
#result = fig.to_plotly_json() 
fig.write_json(file="./plotlyjs/data.json")


