import streamlit as st
import pandas as pd
from helsinki_tickers import helsinki_tickers

st.title("📈 Helsingin pörssin osake-ennusteet")

try:
    df = pd.read_csv("ennusteet.csv")
except Exception as e:
    st.error(f"Virhe tiedoston lukemisessa: {e}")
    st.stop()

# ✅ Näytä vain halutut osakkeet
halutut_tickerit = list(helsinki_tickers.values())
df = df[df["Ticker"].isin(halutut_tickerit)]

valittu = st.selectbox("Valitse osake", df["Ticker"].unique())

valinta = df[df["Ticker"] == valittu].iloc[0]
st.metric("Nyt", f"{valinta['Nyt']} €")
st.metric("Viikon päästä", f"{valinta['Viikko']} €")
st.metric("Kuukauden päästä", f"{valinta['Kuukausi']} €")
