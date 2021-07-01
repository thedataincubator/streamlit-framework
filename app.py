import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
import os
#st.title('TDI Milestone Project')
#st.header('Select Plot Parameters')

Ticker = st.selectbox('Ticker', options =
                  ['IBM',
                   'TSLA',
                   ])
Year = st.selectbox('Year', options =
                  ['Select',2010,
                   2011,
                   2012,
                   2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
Month = st.selectbox('Month:', options =
                  ['Select','January',
                   'February',
                   'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
                   ])
while Year == 'Select' or Month == 'Select':
    continue
load_dotenv()
api_key = '7BVCOMX48DYGXDOY'
ts = TimeSeries(key='7BVCOMX48DYGXDOY', output_format='pandas')
data, meta_data = ts.get_daily(Ticker, outputsize = 'full')
print(meta_data)
month_dict = {}
keys = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12]
i = 0
for key in keys:
    month_dict[key] = values[i]
    i = i+1
y = 2021

m_int = month_dict.get(Month)
data['date'] = data.index.time
s = (data['date'].index.year == Year) * (data['date'].index.month == 4)
g = data[s]['4. close']
st.write(g)
st.line_chart(g)
plt.show()






