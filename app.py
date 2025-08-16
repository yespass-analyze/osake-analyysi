import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime
import plotly.graph_objs as go

# 📥 Käyttäjän syöte
st.title("📊 Osakeanalyysi & Ennusteet")
ticker = st.text_input("Syötä osaketunnus (esim. AAPL, TSLA, NOKIA)", "AAPL")

if ticker:
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df.reset_index(inplace=True)

    # 📈 RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # 📈 MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 📈 Bollinger Bands
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['Upper'] = df['MA20'] + 2 * df['Close'].rolling(window=20).std()
    df['Lower'] = df['MA20'] - 2 * df['Close'].rolling(window=20).std()

    # 🔮 Prophet-ennuste
    forecast_df = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    model = Prophet()
    model.fit(forecast_df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # 📊 PE-luku
    try:
        pe_ratio = stock.info['trailingPE']
    except:
        pe_ratio = "Ei saatavilla"

    # 🎨 Näytetään graafit
    st.subheader("📈 Hintakehitys & Indikaattorit")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Upper'], name='Upper Band', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Lower'], name='Lower Band', line=dict(dash='dot')))
    st.plotly_chart(fig)

    st.subheader("🔮 Ennuste (30 päivää)")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Ennuste'))
    fig2.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Yläraja', line=dict(dash='dot')))
    fig2.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Alaraja', line=dict(dash='dot')))
    st.plotly_chart(fig2)

    # 💡 Suosituslogiikka
    latest_rsi = df['RSI'].iloc[-1]
    latest_macd = df['MACD'].iloc[-1]
    latest_signal = df['Signal'].iloc[-1]

    st.subheader("💡 Suositus")
    if latest_rsi < 30 and latest_macd > latest_signal:
        st.success("Mahdollinen ostopaikka (RSI < 30 ja MACD nousee)")
    elif latest_rsi > 70 and latest_macd < latest_signal:
        st.warning("Mahdollinen myyntipaikka (RSI > 70 ja MACD laskee)")
    else:
        st.info("Ei selkeää signaalia – seuraa tilannetta")

    st.subheader("📊 PE-luku")
    st.write(f"PE-luku: {pe_ratio}")
