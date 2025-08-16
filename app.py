import streamlit as st
import pandas as pd
import json

# Lataa JSON-data
with open("scored_osakkeet.json", "r") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Ulkoasu
st.set_page_config(page_title="Osakepisteytys", layout="wide")
st.title("📊 Osakepisteytys")
st.markdown("""
Tämä työkalu arvioi osakkeet ja antaa niille pisteet 0–100 perustuen koneoppimismalliin.
Korkeampi piste tarkoittaa suurempaa todennäköisyyttä tuottoon.
""")

# 🔝 Parhaat sijoituskohteet
st.subheader("🔝 Parhaat sijoituskohteet")
top_stocks = df.sort_values("score", ascending=False).head(5)
st.table(top_stocks[["name", "score"]])

# 📋 Kaikki osakkeet taulukossa
st.subheader("📋 Kaikki osakkeet")

# Värikoodaus pisteiden mukaan
def highlight_scores(val):
    if val >= 80:
        return "background-color: lightgreen"
    elif val >= 50:
        return "background-color: lightyellow"
    else:
        return "background-color: lightcoral"

styled_df = df.sort_values("score", ascending=False).style.applymap(highlight_scores, subset=["score"])
st.dataframe(styled_df, use_container_width=True)
