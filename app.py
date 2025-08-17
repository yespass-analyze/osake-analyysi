import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nokia_graafi import piirra_graafi
from nokia_tunnusluvut_graafi import piirra_tunnusluvut_graafi
from trendline import plot_trendlines

# 1) Ladataan data (sisältää oletuksena myös 'Signal'-sarake)
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", parse_dates=["Date"], index_col="Date")
    df.sort_index(inplace=True)
    return df

df = lataa_data()

# 2) Sovelluksen otsikko
st.title("📊 Nokian osakeanalyysi")

# 3) Dynaamiset päivärajat
min_date = df.index.min().date()
max_date = df.index.max().date()
alku = st.date_input("Valitse alkupäivä", value=min_date, min_value=min_date, max_value=max_date)
loppu = st.date_input("Valitse loppupäivä", value=max_date, min_value=min_date, max_value=max_date)
df_valittu = df.loc[alku:loppu]

# 4) Valitaan sarake ja näytetään osakekurssin kehittyminen
st.subheader("📈 Osakekurssin kehitys")
sarake = st.selectbox("Valitse sarake:", df.columns, index=df.columns.get_loc("Close"))
fig1 = piirra_graafi(df_valittu, sarake, f"Nokia – {sarake}", signal_col="Signal")
st.pyplot(fig1)

# 5) Ostosuositus-/myyntisuositus tekstinä
if "Signal" in df_valittu.columns:
    viimeisin = df_valittu["Signal"].iloc[-1]
    st.markdown(f"**Viimeisin signaali:** {viimeisin}")
else:
    st.markdown("Signaalit-saraketta ei löytynyt datasta.")

# 6) Tunnusluvut ja trendiviiva
st.subheader("📊 Tunnusluvut")
fig2 = piirra_tunnusluvut_graafi()
st.pyplot(fig2)

st.subheader("📉 Trendiviiva")
fig3 = plot_trendlines(df_valittu)
st.pyplot(fig3)

# 7) Raakadata
with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_valittu)
