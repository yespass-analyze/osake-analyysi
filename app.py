import streamlit as st
import pandas as pd
from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines

# Datan lataus
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", parse_dates=["Date"], index_col="Date")
    df.sort_index(inplace=True)
    return df

df = lataa_data()

# Sovelluksen otsikko
st.title("📊 Nokian osakeanalyysi")

# Valinta: mitä graafeja näytetään
valinta = st.multiselect(
    "Valitse näytettävät graafit:",
    ["Osakekurssi", "Tunnusluvut", "Trendiviiva"],
    default=["Osakekurssi", "Tunnusluvut"]
)

# Osakekurssin graafi
if "Osakekurssi" in valinta:
    st.subheader("📈 Osakekurssin kehitys")
    sarake = st.selectbox("Valitse sarake:", df.columns, index=df.columns.get_loc("Close"))
    fig1 = piirra_graafi(df, sarake, f"Nokia - {sarake}")
    st.pyplot(fig1)

# Tunnuslukugraafi
if "Tunnusluvut" in valinta:
    st.subheader("📊 Tunnusluvut")
    fig2 = piirra_tunnusluvut_graafi()
    st.pyplot(fig2)

# Trendiviiva
if "Trendiviiva" in valinta:
    st.subheader("📉 Trendiviiva")
    fig3 = plot_trendlines(df)
    st.pyplot(fig3)

# Näytä raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df)
