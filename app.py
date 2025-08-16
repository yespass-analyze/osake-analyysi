import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Osakeanalyysi", layout="wide")

st.title("📈 Osakeanalyysi-sovellus")
st.write("Syötä osakkeen ticker (esim. `AAPL`, `NOKIA.HE`) ja valitse aikaväli.")

# Sidebar
ticker = st.sidebar.text_input("Osakkeen ticker", value="NOKIA.HE")
start_date = st.sidebar.date_input("Alkupäivämäärä", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("Loppupäivämäärä", value=pd.to_datetime("today"))

# Lataa data
try:
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.warning("Ei löytynyt dataa annetulla tickerillä.")
    else:
        st.subheader(f"📊 {ticker} - Hintadata")
        st.line_chart(data["Close"])

        st.subheader("📋 Päivittäinen hintadata")
        st.dataframe(data[["Open", "High", "Low", "Close", "Volume"]].tail(20))

        st.subheader("📉 Liukuva keskiarvo")
        ma_period = st.slider("Liukuvan keskiarvon pituus (päivää)", 5, 50, 20)
        data["MA"] = data["Close"].rolling(ma_period).mean()
        st.line_chart(data[["Close", "MA"]])
except Exception as e:
    st.error(f"Tapahtui virhe: {e}")
