import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

@st.cache_data
def lataa_data():
    # 1) Ladataan CSV ja parsitaan Date-kenttä suoraan datetimeksi
    df = pd.read_csv(
        "nokia.csv",
        parse_dates=["Date"],
        dayfirst=True,       # jos päivämäärät muodossa DD.MM.YYYY
        infer_datetime_format=True
    )
    df = df.dropna(subset=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)

    # 2) Varmistetaan, että indeksi on DatetimeIndex
    df.index = pd.to_datetime(df.index)

    return df

df = lataa_data()
if df.empty:
    st.error("🛑 `nokia.csv` on tyhjä tai Date-kentässä on virheitä.")
    st.stop()

# 3) Aikavälikartoitus: päivät
period_map = {
    "1pv":   1,
    "1v":   365,
    "1kk":   30,
    "3kk":   90,
    "6kk":  180,
    "12kk": 365,
    "36kk":1095,
    "60kk":1825
}

valinta = st.selectbox(
    "Valitse aikaväli:",
    options=list(period_map.keys()),
    index=list(period_map.keys()).index("3kk")
)

days = period_map[valinta]

# 4) Lasketaan cut-off päivämäärä ja suodatetaan
last_date = df.index.max()                      # Tämä on nyt pd.Timestamp
start_date = last_date - pd.Timedelta(days=days)
df_valittu = df[df.index >= start_date]

# ---- Sovelluksen UI ----

st.title("📊 Nokian osakeanalyysi")

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
