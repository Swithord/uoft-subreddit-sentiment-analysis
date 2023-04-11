import plotly.express as px
import pandas as pd

df = pd.read_csv('results.csv')

fig = px.bar(df, x='College', y='Mean Sentiment Score', text='n', template='plotly_dark',
             color_discrete_sequence=['#6200ee']*len(df))
fig.update_layout(width=900, height=500, bargap=0.15)
fig.show()
