# app.py

import streamlit as st
from PIL import Image
from nokia_analyysi import arvioi_osto_myynti
import os

st.set_page_config(page_title="Nokia-analyysi", layout="wide")
st.title("📊 Nokian osakeanalyysi")

# Simuloitu data
hinta = 3.61
trendilinja = 3.52
rsi = 49.78
uutisvirta = "Q4 tulos vahva, ohjeistus neutraali"

# Suositus
tulos = arvioi_osto_myynti(hinta, trendilinja, rsi, uutisvirta)

st.subheader("📌 Osto-/myyntisuositus")
st.markdown(f"""
- **Suositus**: {tulos['suositus']}
- **Trendisuunta**: {tulos['suunta']}
- **RSI-tulkinta**: {tulos['rsi_tulkinta']}
- **Uutisvirta**: {tulos['uutis_tulkinta']}
""")

# Graafit
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Hinta vs Trendilinja")
    if os.path.exists("nokia_stock_trend_signals_2025.png"):
        st.image("nokia_stock_trend_signals_2025.png")
    else:
        st.warning("Trendigraafi puuttuu. Aja nokia_graafi.py ensin.")

with col2:
    st.subheader("📊 Tunnusluvut vs Sektori")
    if os.path.exists("nokia_tunnusluvut_vs_sektori.png"):
        st.image("nokia_tunnusluvut_vs_sektori.png")
    else:
        st.warning("Tunnuslukugraafi puuttuu. Aja nokia_tunnusluvut_graafi.py ensin.")
