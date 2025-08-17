# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nokia_analyysi import arvioi_osto_myynti
from trendline import plot_trendlines
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from nokia_graafi import piirra_graafi

st.set_page_config(page_title="📊 Nokia-analyysityökalu", layout="wide")
st.title("📈 Nokian osakeanalyysi")

# --- Aikavälin valinta ---
period = st.selectbox("Valitse aikaväli", ["1mo", "3mo", "6mo", "12mo", "36mo"])
period_map = {
    "1mo": "1mo",
    "3mo": "3mo",
    "6mo": "6mo",
    "12mo": "1y",
    "36mo": "3y"
}

# --- Datan haku ---
import yfinance as yf
ticker = yf.Ticker("NOKIA.HE")
df = ticker.history(period=period_map[period])
df.reset_index(inplace=True)

if df.empty:
    st.warning("Ei löytynyt dataa valitulle aikavälille.")
else:
    st.subheader("📊 Hintadata")
    st.dataframe(df[["Date", "Close"]])

    # --- Trendiviivat + graafi ---
    fig1 = plot_trendlines(df)
    st.pyplot(fig1)

    # --- RSI-laskenta ---
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1] if not rsi.empty else 50

    # --- Suosituslogiikka ---
    hinta = df["Close"].iloc[-1]
    x = np.arange(len(df["Close"]))
    z = np.polyfit(x, df["Close"].values, 1)
    trend = np.poly1d(z)
    trend_arvo = trend(len(df["Close"]) - 1)
    uutisvirta = "Q2 tulos vahva, ohjeistus neutraali"

    tulos = arvioi_osto_myynti(hinta, trend_arvo, latest_rsi, uutisvirta)

    st.subheader("📌 Osto-/myyntisuositus")
    st.markdown(f"""
    - **Suositus**: {tulos['suositus']}
    - **Trendisuunta**: {tulos['suunta']}
    - **RSI-tulkinta**: {tulos['rsi_tulkinta']}
    - **Uutisvirta**: {tulos['uutis_tulkinta']}
    """)

    # --- Tunnusluvut vs sektori ---
    st.subheader("📊 Tunnusluvut vs Sektori")
    fig2 = piirra_tunnusluvut_graafi()
    st.pyplot(fig2)

    # --- Osto-/myyntipisteet ---
    st.subheader("📈 Osto- ja myyntipisteet")
    hinnat = df["Close"].tolist()
    trendilinja = trend(x).tolist()
    ostopisteet = {i: hinnat[i] for i in range(1, len(hinnat)) if hinnat[i] > trendilinja[i] and hinnat[i-1] <= trendilinja[i-1]}
    myyntipisteet = {i: hinnat[i] for i in range(1, len(hinnat)) if hinnat[i] < trendilinja[i] and hinnat[i-1] >= trendilinja[i-1]}
    fig3 = piirra_graafi(hinnat, trendilinja, ostopisteet, myyntipisteet)
    st.pyplot(fig3)
