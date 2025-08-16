import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Helsingin Pörssin Analyysi", layout="wide")
st.title("📈 Helsingin Pörssin Top 10 Sijoituskohdetta")

# 📅 Aikavälin valinta
period = st.selectbox("Valitse analyysin aikaväli", ["1mo", "3mo", "6mo"], index=0)

# 📁 Helsingin pörssin tickerit (voit laajentaa listaa)
helsinki_tickers = {
    "Nokia": "NOKIA.HE",
    "Neste": "NESTE.HE",
    "Fortum": "FORTUM.HE",
    "Kone": "KNEBV.HE",
    "UPM-Kymmene": "UPM.HE",
    "Sampo": "SAMPO.HE",
    "Kesko": "KESKOA.HE",
    "Outokumpu": "OUT1V.HE",
    "Metso": "METSO.HE",
    "Orion": "ORNBV.HE",
    "Valmet": "VALMT.HE",
    "Wärtsilä": "WRT1V.HE",
    "Elisa": "ELISA.HE",
    "Terveystalo": "TTALO.HE",
    "Harvia": "HARVIA.HE",
    "Revenio": "REG1V.HE",
    "Qt Group": "QTCOM.HE",
    "Marimekko": "MMO1V.HE"
}

# 📊 Analyysitulokset
results = []

st.info("Analysoidaan osakkeet... Tämä voi kestää hetken.")

for name, ticker in helsinki_tickers.items():
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period=period)

        if hist.empty or "Close" not in hist.columns:
            continue

        # 📈 Tuotto-odotus
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        return_pct = ((end_price - start_price) / start_price) * 100

        # 📋 Tunnusluvut
        pe = info.get("trailingPE", None)
        dividend = info.get("dividendYield", 0)
        market_cap = info.get("marketCap", 0)
        debt_to_equity = info.get("debtToEquity", None)
        revenue_growth = info.get("revenueGrowth", 0)

        # 🧠 Pisteytys (yksinkertainen malli)
        score = (
            return_pct * 0.4 +
            (1 / pe if pe and pe > 0 else 0) * 20 +
            dividend * 100 * 0.15 +
            revenue_growth * 100 * 0.15 +
            (1 / debt_to_equity if debt_to_equity and debt_to_equity > 0 else 0) * 10
        )

        results.append({
            "Yritys": name,
            "Ticker": ticker,
            "Tuotto (%)": round(return_pct, 2),
            "PE-luku": round(pe, 2) if pe else "–",
            "Osinkotuotto (%)": round(dividend * 100, 2) if dividend else "–",
            "Markkina-arvo": f"{market_cap:,}",
            "Velka/Oma pääoma": round(debt_to_equity, 2) if debt_to_equity else "–",
            "Liikevaihdon kasvu (%)": round(revenue_growth * 100, 2),
            "Pisteet": round(score, 2)
        })

    except Exception as e:
        st.warning(f"Virhe osakkeessa {name}: {e}")
        continue

# 📊 Top 10 osaketta
df = pd.DataFrame(results)
top10 = df.sort_values("Pisteet", ascending=False).head(10)

st.subheader("🔟 Top 10 osaketta sijoitettavaksi")
st.dataframe(top10)

# 📋 Raportti + 📉 Kaavio
for _, row in top10.iterrows():
    st.markdown(f"### 📌 {row['Yritys']} ({row['Ticker']})")
    st.write(f"**Tuotto-odotus ({period}):** {row['Tuotto (%)']}%")
    st.write(f"**PE-luku:** {row['PE-luku']}")
    st.write(f"**Osinkotuotto:** {row['Osinkotuotto (%)']}%")
    st.write(f"**Velka/Oma pääoma:** {row['Velka/Oma pääoma']}")
    st.write(f"**Liikevaihdon kasvu:** {row['Liikevaihdon kasvu (%)']}%")
    st.write(f"**Markkina-arvo:** {row['Markkina-arvo']}")
    st.write(f"**Pisteet:** {row['Pisteet']}")

    # 📉 Kurssikäyrä
    try:
        stock = yf.Ticker(row["Ticker"])
        hist = stock.history(period=period)
        fig, ax = plt.subplots()
        ax.plot(hist.index, hist["Close"], label="Päätöskurssi", color="green")
        ax.set_title(f"{row['Yritys']} ({period})")
        ax.set_xlabel("Päivämäärä")
        ax.set_ylabel("Kurssi (€)")
        ax.legend()
        st.pyplot(fig)
    except:
        st.warning("Kaavion lataus epäonnistui.")
