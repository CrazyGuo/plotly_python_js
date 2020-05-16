# x and y given as DataFrame columns
import plotly.express as px
df = px.data.iris() # iris is a pandas DataFrame
print(df)
fig = px.scatter(df, x="sepal_width", y="sepal_length")

fig.write_json(file="./plotlyjs/data.json")


