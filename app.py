import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import requests
import os

st.title('TDI Milestone Project')
st.header('Select Plot Parameters')
st.text('An interactive chart of stock closing prices using Streamlit and Plot.ly.')

Ticker = st.selectbox('Ticker', options =
                  ['IBM',
                   'TSLA',
                   'AAPL'])
Year = st.selectbox('Year', options =
                  [2010,
                   2011,
                   2012,
                   2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
Month = st.selectbox('Month:', options =
                  ['January',
                   'February',
                   'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
@st.cache
def load_data(Tic, YEAR, MONTH):
    load_dotenv()
    api_key = '7BVCOMX48DYGXDOY'
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_dats = ts.get_daily(Tic, outputsize = 'full')
    month_dict = {}
    keys = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    values = list(range(1, 13))
    i = 0
    for key in keys:
        month_dict[key] = values[i]
        i = i+1
    m_int = month_dict.get(MONTH)
    data['date'] = data.index.time
    s = (data['date'].index.year == YEAR) * (data['date'].index.month == m_int)
    g = data[s]['4. close']
    return g

#### Chart ###
fig = px.line(load_data(Ticker, Year, Month),
                y='4. close',
                )
fig.update_layout(
    xaxis_title="Timestamp",
    yaxis_title="Closing Price",
)
st.plotly_chart(fig)






