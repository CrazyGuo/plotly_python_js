﻿import plotly.express as px

data_canada = px.data.gapminder().query("country == 'Canada'")
print(data_canada)
fig = px.bar(data_canada, x='year', y='pop')

fig.write_json(file="./plotlyjs/data.json")


