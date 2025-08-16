import streamlit as st
import yfinance as yf
import pandas as pd
import joblib
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import matplotlib.pyplot as plt

st.set_page_config(page_title="Short-työkalu", layout="wide")
st.title("📉 Short-työkalu: Helsingin Pörssin riskikohteet")

model = joblib.load("short_model.pkl")

tickers = {
    "Nokia": "NOKIA.HE", "Sampo": "SAMPO.HE", "Neste": "NESTE.HE", "Fortum": "FORTUM.HE",
    "Kone": "KNEBV.HE", "UPM": "UPM.HE", "Stora Enso": "STERV.HE", "Metso": "METSO.HE",
    "Kesko": "KESKOA.HE", "Elisa": "ELISA.HE", "Orion": "ORNBV.HE", "Valmet": "VALMT.HE",
    "Wärtsilä": "WRT1V.HE", "Outokumpu": "OUT1V.HE", "Metsä Board": "METSB.HE", "Kojamo": "KOJAMO.HE",
    "Sanoma": "SANOMA.HE", "Cargotec": "CGCBV.HE", "Konecranes": "KCR.HE", "Terveystalo": "TTALO.HE",
    "Qt Group": "QTCOM.HE", "Revenio": "REG1V.HE", "F-Secure": "FSECURE.HE", "Harvia": "HARVIA.HE",
    "SRV Yhtiöt": "SRV1V.HE", "Tokmanni": "TOKMAN.HE", "Verkkokauppa.com": "VERK.HE", "Ponsse": "PON1V.HE",
    "Etteplan": "ETTE.HE", "Talenom": "TNOM.HE", "Evli": "EVLI.HE", "Marimekko": "MMO1V.HE",
    "Atria": "ATRAV.HE", "HKScan": "HKSAV.HE", "Kemira": "KEMIRA.HE", "Oriola": "ORION.HE",
    "Bittium": "BITTI.HE", "Exel Composites": "EXL1V.HE", "Glaston": "GLAST.HE", "Incap": "INCAP.HE",
    "Scanfil": "SCANFL.HE", "Aspo": "ASPO.HE", "Raute": "RAUTE.HE", "Lehto Group": "LEHTO.HE",
    "Sitowise": "SITOWS.HE", "Dovre Group": "DOV1V.HE", "Consti": "CONSTI.HE", "Endomines": "ENDOM.HE",
    "Componenta": "COMP.HE", "Afarak Group": "AFAGR.HE"
}

results = []
skipped = []

for name, ticker in tickers.items():
    try:
        data = yf.download(ticker, period="2mo", interval="1d")
        data.dropna(inplace=True)

        if len(data) < 20:
            skipped.append((name, "Liian vähän dataa"))
            continue

        close = data["Close"]
        volume = data["Volume"]

        data["rsi"] = RSIIndicator(close=close).rsi()
        data["macd"] = MACD(close=close).macd_diff()
        data["bollinger"] = BollingerBands(close=close).bollinger_hband()
        data["ema"] = EMAIndicator(close=close).ema_indicator()
        data["obv"] = OnBalanceVolumeIndicator(close=close, volume=volume).on_balance_volume()
        data["momentum"] = close.diff()
        data["volatility"] = close.pct_change().rolling(window=5).std()

        data.dropna(inplace=True)
        if len(data) == 0:
            skipped.append((name, "Indikaattorit eivät ehtineet laskea"))
            continue

        latest = data.iloc[-1]
        X = pd.DataFrame([latest[["rsi", "macd", "bollinger", "ema", "obv", "momentum", "volatility"]]])
        prob = model.predict_proba(X)[0][1]
        score = round(prob * 100, 1)

        results.append({
            "Yritys": name,
            "Ticker": ticker,
            "Todennäköisyys laskulle (>2%)": f"{score}%",
            "RSI": round(latest["rsi"], 2),
            "MACD": round(latest["macd"], 2),
            "Momentum": round(latest["momentum"], 2),
            "Volatiliteetti": round(latest["volatility"], 2),
            "Pisteet": score
        })

    except Exception as e:
        skipped.append((name, str(e)))
        continue

df = pd.DataFrame(results).sort_values("Pisteet", ascending=False)

st.subheader("🔝 Top short-kohteet")
st.dataframe(df, use_container_width=True)

if skipped:
    st.subheader("⚠️ Ohitetut osakkeet")
    st.write(pd.DataFrame(skipped, columns=["Yritys", "Syy"]))

for _, row in df.head(5).iterrows():
    st.markdown(f"### 📉 {row['Yritys']} ({row['Ticker']})")
    try:
        hist = yf.download(row["Ticker"], period="2mo", interval="1d")
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist["Close"], label="Kurssi", color="red")
        ax.set_title(f"{row['Yritys']} - Kurssikäyrä")
        ax.set_xlabel("Päivämäärä")
        ax.set_ylabel("Kurssi (€)")
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Kaavion lataus epäonnistui.")
