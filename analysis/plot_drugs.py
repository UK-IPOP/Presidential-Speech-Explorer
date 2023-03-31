import pandas as pd
import plotly.express as px
import polars as pl


df = pl.read_csv("./output.csv")

# exact matches only
drugs = df.filter(pl.col("Similarity Score") == 1.0)
print(drugs.head())


speeches = pl.read_csv("./speech_table.csv")
print(speeches.head())

df = pd.merge(
    drugs.to_pandas(),
    speeches.to_pandas(),
    left_on='Row ID',
    right_on='index',
)
df.drop(columns=['Source Column', 'Similarity Score'], inplace=True)

del speeches, drugs
df['date'] = pd.to_datetime(df['date'])
print(df.head())

groups = df.groupby([pd.Grouper(key='date', freq='M'), 'Search Term']).size().reset_index().rename(columns={0: 'count'})
print(groups)
print(groups.dtypes)
fig = px.line(
    groups,
    x='date',
    y='count',
    color='Search Term',
)
fig.write_html("drugs_timeseries.html")
fig.show()
