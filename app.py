import streamlit as st
import pandas as pd
from trendline import plot_trendlines

st.set_page_config(page_title="📈 Osakesovellus", layout="wide")

st.title("📊 Osakesovellus")
st.markdown("Syötä osakedataa ja tarkastele trendiviivoja sekä tapahtumahistoriaa.")

# --- Datan lataus ---
uploaded_file = st.file_uploader("📂 Lataa CSV-tiedosto (sisältää 'Date' ja 'Close')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    df = df.sort_values("Date")
    st.success("Data ladattu onnistuneesti!")
    st.dataframe(df)

    # --- Trendiviivat ---
    plot_trendlines(df)

    # --- Tapahtumien syöttö ---
    st.subheader("📥 Syötä osto- ja myyntitapahtumia")

    transaction_type = st.selectbox("Tapahtuman tyyppi", ["Osto", "Myynti"])
    date = st.date_input("Päivämäärä")
    price = st.number_input("Hinta", min_value=0.0, format="%.2f")
    quantity = st.number_input("Määrä", min_value=1)

    if st.button("Lisää tapahtuma"):
        new_transaction = {
            "Tyyppi": transaction_type,
            "Päivämäärä": date,
            "Hinta": price,
            "Määrä": quantity
        }

        if "transactions" not in st.session_state:
            st.session_state.transactions = []

        st.session_state.transactions.append(new_transaction)
        st.success("✅ Tapahtuma lisätty!")

    # --- Tapahtumien näyttö ---
    if "transactions" in st.session_state and st.session_state.transactions:
        st.subheader("📊 Tapahtumahistoria")
        st.dataframe(pd.DataFrame(st.session_state.transactions))
else:
    st.info("Lataa CSV-tiedosto aloittaaksesi.")
