#%%

import streamlit as st
import numpy as np
import pandas as pd
st.title('Garrick Bruening TDI Milestone')
import csv
import requests
import plotly.express as px
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from dotenv import load_dotenv, dotenv_values
config_vars = dotenv_values('config.env')
api_key = config_vars['api_key']

ticker_select = st.sidebar.text_input('What ticker?', 'IBM')
start_select = st.sidebar.date_input('Start Date', datetime.date(2021, 1, 1))
end_select = st.sidebar.date_input('End Date', datetime.date(2021, 2, 1))

@st.cache
def get_data(ticker_select):
    ticker = ticker_select
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}&outputsize=full'.format(ticker, api_key)
    response = requests.get(url)
    json_file = response.json()
    test = pd.DataFrame.from_dict(json_file['Time Series (Daily)'],orient='index')
    test.columns = test.columns.str[3:]
    test = test.astype(np.float64)
    test['date'] = test.index
    test['date'] = pd.to_datetime(test['date'])
    # test = test.query('low < 150')
    return test

def filter_data(df, start_select, end_select):
    df = df.loc[(df['date']>=start_select.strftime('%Y-%m-%d')) & (df['date']<=end_select.strftime('%Y-%m-%d'))]
    return df

test = filter_data(get_data(ticker_select), start_select, end_select)

df1 = test.melt(id_vars=['date']+list(test.keys()[0:4]), var_name=ticker_select)

fig = px.line(test,
                x = 'date',
                y = ['open','close','high','low'],
                title = 'Opening Stock prices by day for '+str(ticker_select))
fig.update_xaxes(title_text = 'Date')
fig.update_yaxes(title_text = 'USD ($)')
fig.update_layout(
    transition_duration = 500
)

fig2 = px.line(test,
                x = 'date',
                y = 'volume',
                title = 'Volume of stock by day for '+ str(ticker_select))
fig2.update_xaxes(title_text = 'Date')
fig2.update_yaxes(title_text = 'Volume (Millions)')
fig2.update_layout(
    transition_duration = 500
)

fig.update_layout(
    transition_duration = 500
)

st.plotly_chart(fig)
st.plotly_chart(fig2)

# %%
