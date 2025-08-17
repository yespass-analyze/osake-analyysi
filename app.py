import streamlit as st
import pandas as pd
from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines
from ostosuositus import arvioi_ostosuositus

# Datan lataus
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", parse_dates=["Date"], index_col="Date")
    df.sort_index(inplace=True)
    return df

df = lataa_data()

st.title("📊 Nokian osakeanalyysi")

# Aikavälin valinta
min_date = df.index.min()
max_date = df.index.max()

alku = st.date_input("Valitse alkupäivä", min_value=min_date, max_value=max_date, value=min_date)
loppu = st.date_input("Valitse loppupäivä", min_value=min_date, max_value=max_date, value=max_date)

df_valittu = df.loc[(df.index >= pd.to_datetime(alku)) & (df.index <= pd.to_datetime(loppu))]

# Osakekurssin graafi
st.subheader("📈 Osakekurssin kehitys")
fig1 = piirra_graafi(df_valittu, 'Close', 'Nokia - Close')
st.pyplot(fig1)

# Ostosuositus
suositus = arvioi_ostosuositus(df_valittu)
st.markdown(f"**Ostosuositus:** {suositus}")

# Tunnusluvut
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

# Trendiviiva
st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# Raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
