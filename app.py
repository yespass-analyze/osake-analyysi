import streamlit as st
import pandas as pd

from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# 1) Datan lataus ja Date-index-muunnos
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv")
    # Muunnetaan Date- ja asetetaan indeksiksi
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df

df = lataa_data()

# 2) Dynaamiset minim ja maksimi datasta
#    käytämme pelkästään Timestamp-objektia, joka toimii date_inputissa
min_date = df.index.min()
max_date = df.index.max()

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

# 3) Suodatettu data aikavälille
#    date_input palauttaa datetime.date, joten vertailu onnistuu suoraan
df_valittu = df.loc[alku : loppu]

# 4) Sovelluksen otsikko
st.title("📊 Nokian osakeanalyysi")

# 5) Osakekurssi + signaalit
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

# 6) Tekstimuotoinen ostos-/myyntisuositus
st.subheader("💡 Suositus")
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**{suositus}**")

# 7) Tunnusluvut
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

# 8) Trendiviiva
st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# 9) Raakadata laajennettuna
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
