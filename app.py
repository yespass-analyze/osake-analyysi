import streamlit as st
import yfinance as yf
import pandas as pd
import joblib
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator

st.set_page_config(page_title="Short-ennustaja", layout="wide")
st.title("🔮 Short-ennustaja: Helsingin Pörssin riskikohteet")

model = joblib.load("short_model.pkl")

tickers = {
    "Nokia": "NOKIA.HE", "Sampo": "SAMPO.HE", "Neste": "NESTE.HE", "Fortum": "FORTUM.HE",
    "Kone": "KNEBV.HE", "UPM": "UPM.HE", "Stora Enso": "STERV.HE", "Metso": "METSO.HE",
    "Kesko": "KESKOA.HE", "Elisa": "ELISA.HE"
}

results = []

for name, ticker in tickers.items():
    try:
        data = yf.download(ticker, period="2mo", interval="1d")
        data.dropna(inplace=True)

        close = data["Close"].squeeze()
        volume = data["Volume"].squeeze()

        data["rsi"] = RSIIndicator(close=close).rsi()
        data["macd"] = MACD(close=close).macd_diff()
        data["bollinger"] = BollingerBands(close=close).bollinger_hband()
        data["ema"] = EMAIndicator(close=close).ema_indicator()
        data["obv"] = OnBalanceVolumeIndicator(close=close, volume=volume).on_balance_volume()
        data["momentum"] = close.diff()

        latest = data.iloc[-1]
        X = pd.DataFrame([latest[["rsi", "macd", "bollinger", "ema", "obv", "momentum"]]])
        prob = model.predict_proba(X)[0][1]

        results.append({
            "Yritys": name,
            "Ticker": ticker,
            "Todennäköisyys laskulle (>2%)": f"{prob*100:.1f}%",
            "RSI": round(latest["rsi"], 2),
            "MACD": round(latest["macd"], 2),
            "Momentum": round(latest["momentum"], 2)
        })

    except Exception as e:
        st.warning(f"{name}: {e}")
        continue

df = pd.DataFrame(results).sort_values("Todennäköisyys laskulle (>2%)", ascending=False)
st.subheader("📉 Top short-kohteet")
st.dataframe(df)
