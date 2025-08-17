import streamlit as st
from data_fetcher import get_stock_data
from trendline import plot_trendlines
from indicators import show_indicators
from valuation import show_valuation
from signals import show_signals
from telegram_alerts import check_alerts
from ml_model import predict_price

st.set_page_config(page_title="Nokia-analyysityökalu", layout="wide")
st.title("📊 Nokia (HEL) – Analyysityökalu")

period = st.selectbox("Valitse aikaväli", ["1d", "1mo", "3mo", "6mo", "12mo", "36mo"])
df = get_stock_data(period)
plot_trendlines(df)
show_indicators(df)
show_valuation()
show_signals(df)
predict_price(df)
check_alerts(df)

import streamlit as st
import pandas as pd

def transaction_input():
    st.subheader("📥 Syötä osto- ja myyntitapahtumat")

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
        st.success("Tapahtuma lisätty!")

    if "transactions" in st.session_state:
        st.subheader("📊 Tapahtumahistoria")
        st.dataframe(pd.DataFrame(st.session_state.transactions))
