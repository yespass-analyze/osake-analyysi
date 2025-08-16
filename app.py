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
""")

# Parhaat osakkeet
top_stocks = df.sort_values("score", ascending=False).head(5)
st.subheader("🔝 Parhaat sijoituskohteet")
st.table(top_stocks[["name", "score"]])

# Kaikki osakkeet
st.subheader("📋 Kaikki osakkeet")
st.dataframe(df.sort_values("score", ascending=False), use_container_width=True)
