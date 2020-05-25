import plotly.express as px

data = px.data.gapminder()

data_canada = data[data.country == 'Canada']
#默认对应的x,y轴对应的值会同hover_data一样，悬浮的时候显示，同时labels可以定制字段的显示
fig = px.bar(data_canada, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
             labels={'pop':'population of Canada'}, height=400)

fig.write_json(file="./plotlyjs/data.json")


