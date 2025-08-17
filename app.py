import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", parse_dates=["Date"], dayfirst=True)
    df = df.dropna(subset=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df

df = lataa_data()
if df.empty:
    st.error("🛑 `nokia.csv` on tyhjä tai Date-kentässä on virheitä.")
    st.stop()

# Kartoitus kalenteripäiviin
period_map = {
    "1pv":   1,
    "1v":  365,
    "1kk":  30,
    "3kk":  90,
    "6kk": 180,
    "12kk":365,
    "36kk":1095,
    "60kk":1825
}

valinta = st.selectbox(
    "Valitse aikaväli:",
    options=list(period_map.keys()),
    index=list(period_map.keys()).index("3kk")
)

days = period_map[valinta]
last_date = df.index.max()
start_date = last_date - pd.Timedelta(days=days)
df_valittu = df.loc[start_date:]

st.title("📊 Nokian osakeanalyysi")

st.subheader("📈 Osakekurssi ja signaalit")
sarake = st.selectbox("Valitse sarake graafiin:", options=df.columns, index=df.columns.get_loc("Close"))
fig1 = piirra_graafi(df_valittu, sarake, f"Nokia – {sarake}", signal_col="Signal")
st.pyplot(fig1)

st.subheader("💡 Suositus")
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**{suositus}**")

st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

st.subheader("📉 Trendiviiva ja kanavat")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
