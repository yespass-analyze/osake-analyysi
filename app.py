import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Lue ennusteet
df = pd.read_csv("ennusteet.csv")

st.set_page_config(page_title="Osake-ennusteet", layout="centered")
st.title("📈 Osake-ennusteet")
st.write("Tässä ovat mallien ennusteet eri aikaväleillä:")

# Näytä koko taulukko
st.dataframe(df, use_container_width=True)

# Valitse osake
valinta = st.selectbox("Valitse osake", df["Ticker"].unique())

# Näytä valitun osakkeen rivit
rivi = df[df["Ticker"] == valinta].iloc[0]

st.subheader(f"🔍 Ennusteet osakkeelle {valinta}")
col1, col2, col3 = st.columns(3)
col1.metric("Nyt", f"{rivi['Nyt']:.2f}")
col2.metric("Viikko", f"{rivi['Viikko']:.2f}")
col3.metric("Kuukausi", f"{rivi['Kuukausi']:.2f}")

# 📊 Piirrä ennustekäyrä
st.subheader("📊 Ennustekäyrä")
fig, ax = plt.subplots()
x = ["Nyt", "Viikko", "Kuukausi"]
y = [rivi["Nyt"], rivi["Viikko"], rivi["Kuukausi"]]
ax.plot(x, y, marker="o", linestyle="-", color="blue")
ax.set_ylabel("Ennustettu arvo")
ax.set_title(f"{valinta} - Ennustekehitys")
st.pyplot(fig)
