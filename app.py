import streamlit as st
import pandas as pd

st.title("📊 Helsingin pörssin osake-ennusteet")

try:
    df = pd.read_csv("ennusteet.csv")
except Exception as e:
    st.error(f"Virhe tiedoston lukemisessa: {e}")
    st.stop()

# ✅ Valitse yhtiön nimellä
valittu_nimi = st.selectbox("Valitse yhtiö", df["Nimi"].unique())
valinta = df[df["Nimi"] == valittu_nimi].iloc[0]

st.subheader(f"{valinta['Nimi']} ({valinta['Ticker']})")
st.metric("Nyt", f"{valinta['Nyt']} €")
st.metric("Viikon päästä", f"{valinta['Viikko']} €")
st.metric("Kuukauden päästä", f"{valinta['Kuukausi']} €")
