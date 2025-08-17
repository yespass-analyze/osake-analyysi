import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# 1) Datan lataus ja väliasetukset
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", parse_dates=["Date"], index_col="Date")
    df.sort_index(inplace=True)
    return df

df = lataa_data()

min_date = df.index.min().date()
max_date = df.index.max().date()

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

# Suodatettu data aikavälille
df_valittu = df.loc[alku:loppu]

# 2) Sovelluksen otsikko
st.title("📊 Nokian osakeanalyysi")

# 3) Osakekurssin graafi ja signaalit
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

# 4) Tekstimuotoinen ostos-/myyntisuositus
st.subheader("💡 Suositus")
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**{suositus}**")

# 5) Tunnusluvut
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

# 6) Trendiviiva
st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# 7) Raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
