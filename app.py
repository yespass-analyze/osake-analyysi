import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# 1) Datan lataus ja puhdistus
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv")
    # Muunna Date-pylväs datetime-tyyppiseksi, epäkelvot merkkijonot → NaT
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    # Pudota rivit, joilla Date on NaT
    df = df.dropna(subset=["Date"])
    # Aseta indeksi ja järjestä nousevasti
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df

df = lataa_data()

# 2) Dynaamiset aikarajat (Timestamp-objekteina)
min_date = df.index.min()
max_date = df.index.max()

# 3) Käyttäjän valinnat
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

# 4) Suodatettu data aikavälille
df_valittu = df.loc[alku:loppu]

# 5) Sovelluksen otsikko
st.title("📊 Nokian osakeanalyysi")

# 6) Osakekurssi + ostos-/myyntisignaalit
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

# 7) Tekstimuotoinen suositus
st.subheader("💡 Suositus")
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**{suositus}**")

# 8) Tunnusluvut
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

# 9) Trendiviiva
st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# 10) Raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
