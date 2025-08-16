import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go
from stocknews import StockNews
import datetime

# --- Sivun asetukset ---
st.set_page_config(page_title="Osakeanalyysi", layout="wide")

# --- Tyyli ---
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Tickerin valinta ---
st.title("📊 Osakeanalyysi")
ticker = st.text_input("Syötä osakkeen ticker (esim. NOKIA.HE)", "NOKIA.HE")

# --- Ladataan data ---
stock = yf.Ticker(ticker)
df = stock.history(period="1y")
df.reset_index(inplace=True)

# --- Tekniset indikaattorit ---
df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean()))
df['EMA12'] = df['Close'].ewm(span=12).mean()
df['EMA26'] = df['Close'].ewm(span=26).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['Upper'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std()
df['Lower'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std()

# --- Graafi ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Upper'], name='Upper Band', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Lower'], name='Lower Band', line=dict(dash='dot')))
fig.update_layout(title=f"{ticker} - Bollinger Bands", xaxis_title="Päivämäärä", yaxis_title="Hinta")
st.plotly_chart(fig, use_container_width=True)

# --- PE-luku ja fundat ---
info = stock.info
st.subheader("📚 Fundat")
st.write(f"PE-luku: {info.get('trailingPE', 'Ei saatavilla')}")
st.write(f"Markkina-arvo: {info.get('marketCap', 'Ei saatavilla')}")
st.write(f"Toimiala: {info.get('sector', 'Ei saatavilla')}")

# --- Ennusteet ---
st.subheader("🔮 Ennuste (30 päivää)")
forecast_df = df[['Date', 'Close']].copy()
forecast_df['ds'] = pd.to_datetime(forecast_df['Date']).dt.tz_localize(None)
forecast_df['y'] = forecast_df['Close']
forecast_df = forecast_df[['ds', 'y']]
model = Prophet()
model.fit(forecast_df)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
fig2 = plot_plotly(model, forecast)
st.plotly_chart(fig2, use_container_width=True)

# --- Ostohistoria ---
st.subheader("💰 Ostohistoria")
if "trades" not in st.session_state:
    st.session_state.trades = []

with st.form("trade_form"):
    date = st.date_input("Ostopäivä")
    price = st.number_input("Ostohinta", min_value=0.0)
    quantity = st.number_input("Määrä", min_value=1)
    note = st.text_area("Muistiinpano")
    submit = st.form_submit_button("Lisää ostos")

    if submit:
        st.session_state.trades.append({"date": date, "price": price, "quantity": quantity, "note": note})

if st.session_state.trades:
    trades_df = pd.DataFrame(st.session_state.trades)
    trades_df["Total"] = trades_df["price"] * trades_df["quantity"]
    st.dataframe(trades_df)
    total_cost = trades_df["Total"].sum()
    current_price = df['Close'].iloc[-1]
    current_value = trades_df["quantity"].sum() * current_price
    st.write(f"📈 Nykyarvo: {current_value:.2f} €")
    st.write(f"📉 Voitto/Tappio: {(current_value - total_cost):.2f} €")

# --- Uutiset ---
st.subheader("🗞️ Uutiset")
try:
    sn = StockNews(ticker, save_news=False)
    news = sn.read_rss()
    for i in range(5):
        st.markdown(f"**{news['title'][i]}**")
        st.write(news['published'][i])
        st.write(news['summary'][i])
        st.write(news['link'][i])
except:
    st.write("Uutisia ei voitu hakea.")

# --- Hintahälytys ---
st.subheader("🔔 Hintahälytys")
target_price = st.number_input("Aseta hintaraja", min_value=0.0)
if target_price > 0:
    current_price = df['Close'].iloc[-1]
    if current_price >= target_price:
        st.success(f"Hinta on ylittänyt rajan! ({current_price:.2f} €)")

# --- Inderes-raportit ---
st.subheader("📄 Inderes-raportit")
inderes_url = f"https://www.inderes.fi/fi/yhtiot/{ticker.split('.')[0].lower()}"
st.markdown(f"[Avaa Inderesin raportit]({inderes_url})")

# --- Chatbot ---
st.subheader("💬 Chatbot")
question = st.text_input("Kysy teknisestä indikaattorista (esim. 'Mitä RSI tarkoittaa?')")
if question:
    if "rsi" in question.lower():
        st.info("RSI mittaa osakkeen yliostettua tai ylimyytyä tilaa. Yli 70 = yliostettu, alle 30 = ylimyyty.")
    elif "macd" in question.lower():
        st.info("MACD kertoo trendin suunnasta ja vahvuudesta. Positiivinen MACD = nousutrendi.")
    elif "bollinger" in question.lower():
        st.info("Bollinger Bands näyttää hintavaihtelun ja mahdolliset käännekohdat.")
    else:
        st.info("En osaa vastata tuohon vielä, mutta kehitystä jatketaan!")

