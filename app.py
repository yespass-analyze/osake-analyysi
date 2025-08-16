import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Short-työkalu", layout="wide")
st.title("📉 Short-työkalu: Helsingin Pörssin Top 10 short-kohdetta")

# 📅 Aikavälin valinta
period_map = {
    "1 viikko": "5d",
    "2 viikkoa": "10d",
    "1 kuukausi": "1mo",
    "3 kuukautta": "3mo",
    "6 kuukautta": "6mo",
    "1 vuosi": "1y"
}
period_label = st.selectbox("Valitse aikaväli", list(period_map.keys()))
period = period_map[period_label]

# 📦 Osakkeet
tickers = {
    "Nokia": "NOKIA.HE", "Sampo": "SAMPO.HE", "Neste": "NESTE.HE", "Fortum": "FORTUM.HE",
    "Kone": "KNEBV.HE", "UPM": "UPM.HE", "Stora Enso": "STERV.HE", "Metso": "METSO.HE",
    "Kesko": "KESKOA.HE", "Elisa": "ELISA.HE"
}

results = []
st.info("Analysoidaan osakkeet...")

for name, ticker in tickers.items():
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period=period)

        if hist.empty or "Close" not in hist.columns:
            continue

        # 📉 Tuotto
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        return_pct = ((end_price - start_price) / start_price) * 100

        # 📊 Volatiliteetti
        daily_returns = hist["Close"].pct_change().dropna()
        volatility = daily_returns.std() * 100

        # 📈 RSI
        delta = hist["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_value = rsi.iloc[-1] if not rsi.empty else 0

        # 📉 MACD
        ema12 = hist["Close"].ewm(span=12, adjust=False).mean()
        ema26 = hist["Close"].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        macd_score = 1 if macd.iloc[-1] < signal.iloc[-1] else 0

        # 📊 Bollinger
        ma20 = hist["Close"].rolling(window=20).mean()
        std20 = hist["Close"].rolling(window=20).std()
        upper_band = ma20 + 2 * std20
        bollinger_score = 1 if hist["Close"].iloc[-1] > upper_band.iloc[-1] else 0

        # 🕵️‍♂️ Insider-myynti
        insider_score = 0
        try:
            insider_data = stock.insider_transactions
            recent_sales = insider_data[
                (insider_data["Transaction"] == "Sale") &
                (pd.to_datetime(insider_data["Start Date"]) > pd.Timestamp.now() - pd.Timedelta("90D"))
            ]
            insider_score = 1 if not recent_sales.empty else 0
        except:
            pass

        # 🧠 Pisteytys
        score = (
            (-return_pct) * 0.3 +
            volatility * 0.2 +
            (rsi_value if rsi_value > 70 else 0) * 0.15 +
            macd_score * 10 +
            bollinger_score * 10 +
            insider_score * 15
        )

        results.append({
            "Yritys": name,
            "Ticker": ticker,
            "Tuotto (%)": round(return_pct, 2),
            "Volatiliteetti": round(volatility, 2),
            "RSI": round(rsi_value, 2),
            "MACD < Signaali": "✅" if macd_score else "❌",
            "Bollinger yli": "✅" if bollinger_score else "❌",
            "Insider-myynti": "✅" if insider_score else "❌",
            "Pisteet": round(score, 2)
        })

    except Exception as e:
        st.warning(f"Virhe osakkeessa {name}: {e}")
        continue

df = pd.DataFrame(results)
top10 = df.sort_values("Pisteet", ascending=False).head(10)

st.subheader("🔟 Top 10 short-kohdetta")
st.dataframe(top10)

for _, row in top10.iterrows():
    st.markdown(f"### 📌 {row['Yritys']} ({row['Ticker']})")
    st.write(f"**Tuotto ({period_label}):** {row['Tuotto (%)']}%")
    st.write(f"**Volatiliteetti:** {row['Volatiliteetti']}%")
    st.write(f"**RSI:** {row['RSI']}")
    st.write(f"**MACD < Signaali:** {row['MACD < Signaali']}")
    st.write(f"**Bollinger yli:** {row['Bollinger yli']}")
    st.write(f"**Insider-myynti:** {row['Insider-myynti']}")
    st.write(f"**Pisteet:** {row['Pisteet']}")

    try:
        stock = yf.Ticker(row["Ticker"])
        hist = stock.history(period=period)
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist["Close"], label="Kurssi", color="red")
        ax.set_title(f"{row['Yritys']} ({period_label})")
        ax.set_xlabel("Päivämäärä")
        ax.set_ylabel("Kurssi (€)")
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Kaavion lataus epäonnistui.")
