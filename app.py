import requests
import streamlit as st

ticker = st.text_input("Ticker")
month = st.text_input("Month")
day = st.text_input("Day")
year = st.text_input("Year")

st.text(year + " " + day + " " + month + " " + ticker)

if st.button("Start"):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=5WB3BZG4UX3GQGAH'
    r = requests.get(url)
    data = r.json()

    st.write(data)
else:
    st.write("Not yet started")

