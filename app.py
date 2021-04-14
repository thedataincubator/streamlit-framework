#import yfinance as yf
#from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries 
import streamlit as st
import pandas as pd 
import datetime
import altair as alt
import sys
import plotly.express as px 
import os
from dotenv import load_dotenv

load_dotenv()



@st.cache()
def Data(Ticker):
    API_key = os.environ.get('API')
    allData = TimeSeries(API_key, output_format='pandas')
    data, meta_data= allData.get_monthly(Ticker)
    data.drop(['1. open', '2. high','3. low'], axis=1, inplace=True)
    data.rename(columns={'4. close' : 'price', '5. volume': 'volume'}, inplace=True)
    data.reset_index(level=data.index.names, inplace=True)
    data = data.sort_index(ascending=False)
    data['year'] = data['date'].dt.year
    data['date'] = data['date'].dt.strftime('%b-%Y')
    return data
   

    
 
st.title("MileStone Project")
st.subheader(" Simple stock price app for the Data Incubator prep " )
Ticker = st.text_input('Ticker')
click = st.button("Show Graph")

if click: 
    if Ticker =="":
        st.warning("Please input valid Ticker Sympol")
    
    else:
        print(Ticker)
        try:
            Data = Data(Ticker)
            GraphData= Data[['date', 'price','volume','year']]
            x = GraphData['date'].tolist()
            y = GraphData['price'].tolist()
            st.write(GraphData)
            fig = px.line(GraphData, x= x, y= y )
            fig.update_layout(
            title= Ticker + " Stock Price History",
            xaxis_title="Time Line",
            yaxis_title="Stock Price",
            legend_title="Legend",
            font=dict(
            family="Courier New, monospace",
            size=14,
            color="green")
            )
            st.plotly_chart(fig)
        except:
            st.warning('worng input')
