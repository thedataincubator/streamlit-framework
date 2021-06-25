import requests
import streamlit as st

ticker = st.text_input("Ticker")
month = st.text_input("Month")
year = st.text_input("Year")

st.text(year + " " + month + " " + ticker)

if st.button("Start"):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=5WB3BZG4UX3GQGAH'
    r = requests.get(url)
    data = r.json()

    timeSeries = data["Time Series (Daily)"]

    results = []
    dates = []
    day = 31
    date = ""
    while day > 0:
        if day < 10:
            date = year + "-" + month + "-0" + str(day)
        else:
            date = year + "-" + month + "-" + str(day)

        if date not in timeSeries:
            day = day - 1
            continue

        dayPrices = timeSeries[date]
        closing = dayPrices["4. close"]
        results.append(closing)
        dates.append(date)

        day = day - 1

    st.write(results)
    st.write(dates)
else:
    st.write("Not yet started")
