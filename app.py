import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# 1) Ladataan data ja varmistetaan validit Date-indeksit
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df

df = lataa_data()
if df.empty:
    st.error("🛑 `nokia.csv` on tyhjä tai Date-kentässä on virheitä.")
    st.stop()

# 2) Aikavälin valinta (viimeiset N päivää)
period_map = {
    "1pv":   1,
    "1v":    7,
    "1kk":  30,
    "3kk":  90,
    "6kk": 180,
    "12kk":365,
    "36kk":1095,
    "60kk":1825
}
valinta = st.selectbox(
    "Valitse aikaväli (viimeiset … päivää):",
    options=list(period_map.keys()),
    index=2
)
days = period_map[valinta]
df_valittu = df.last(f"{days}D")

# 3) Sovelluksen runko
st.title("📊 Nokian osakeanalyysi")

# A) Osakekurssin graafi + signaalit
st.subheader("📈 Osakekurssi ja signaalit")
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

# B) Tekstimuotoinen ostos-/myyntisuositus
st.subheader("💡 Suositus")
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
