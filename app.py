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

# Aikavälin valinta
period = st.selectbox("Valitse aikaväli", ["1d", "1m", "3m", "6m", "12m", "36m"])

# Hae data
df = get_stock_data(period)

# Näytä trendilinjat
plot_trendlines(df)

# Näytä tekniset indikaattorit
show_indicators(df)

# Näytä tunnusluvut
show_valuation()

# Näytä osto/myyntivinkit
show_signals(df)

# Ennuste
predict_price(df)

# Telegram-hälytykset
check_alerts(df)
