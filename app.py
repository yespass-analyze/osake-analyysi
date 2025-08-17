# app.py

import streamlit as st
import pandas as pd
from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# 1) Ladataan data ja puhdistetaan Date-sarakkeen virheet
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])                # Pudotetaan rivit, joissa Date on NaT
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df

df = lataa_data()

# 2) Jos data on tyhjä, näytetään viesti ja pysäytetään
if df.empty:
    st.error("🛑 Datakehys on tyhjä. Tarkista `nokia.csv`-tiedosto.")
    st.stop()

# 3) Määritellään min/max päivämäärinä (Python date ‑oliot)
min_ts, max_ts = df.index.min(), df.index.max()
min_date, max_date = min_ts.date(), max_ts.date()

# 4) Käyttäjän valinta aikavälistä
alku = st.date_input(
    "Valitse alkupäivä",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)
loppu = st.date_input(
    "Valitse loppupäivä",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# 5) Suodatetaan data valitulle aikavälille
df_valittu = df.loc[alku : loppu]

# -----------------------
# Pääsisältö Streamlitissä
# -----------------------

st.title("📊 Nokian osakeanalyysi")

# A) Osakekurssin graafi + signaalit
st.subheader("📈 Osakekurssin kehitys ja signaalit")
sarake = st.selectbox(
    "Valitse sarake graafiin:",
    options=df.columns,
    index=df.columns.get_loc("Close")
)
fig1 = piirra_graafi(
    df_valittu,
    sarake=sarake,
    otsikko=f"Nokia – {sarake}",
    signal_col="Signal"
)
st.pyplot(fig1)

# B) Tekstimuotoinen suositus
st.subheader("💡 Osto-/myyntisuositus")
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**{suositus}**")

# C) Tunnusluvut
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

# D) Trendiviiva
st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# E) Raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
