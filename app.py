import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Osakeapp", layout="centered")
st.title("📊 Osakeanalyysi")

# Dynaaminen haku
user_input = st.text_input("🔍 Syötä osakkeen nimi tai ticker (esim. Nokia tai AAPL)", "")

# Tunnetut osakkeet
suggestions = {
    "Nokia": "NOKIA.HE",
    "Neste": "NESTE.HE",
    "Fortum": "FORTUM.HE",
    "Kone": "KNEBV.HE",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google (Alphabet)": "GOOGL",
    "Meta (Facebook)": "META"
}

ticker = suggestions.get(user_input.strip(), user_input.strip().upper())

# 📅 Aikavälin valinta
period = st.selectbox("Valitse aikaväli", ["1mo", "3mo", "6mo", "1y", "5y", "max"], index=3)

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        df = stock.history(period=period)
        df.reset_index(inplace=True)

        st.subheader(f"📌 {info.get('longName', ticker)} ({ticker})")

        # ℹ️ Perustiedot
        st.markdown("### ℹ️ Perustiedot")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Markkina-arvo:** {info.get('marketCap', '–'):,}")
            st.write(f"**PE-luku (TTM):** {info.get('trailingPE', '–')}")
            st.write(f"**Osinkotuotto (%):** {info.get('dividendYield', '–')}")
            st.write(f"**Sektori:** {info.get('sector', '–')}")
        with col2:
            st.write(f"**52v huippu:** {info.get('fiftyTwoWeekHigh', '–')}")
            st.write(f"**52v pohja:** {info.get('fiftyTwoWeekLow', '–')}")
            st.write(f"**Beta:** {info.get('beta', '–')}")
            st.write(f"**P/E Forward:** {info.get('forwardPE', '–')}")

        # 📉 Kurssidata
        st.markdown(f"### 📉 Kurssikehitys ({period})")
        st.dataframe(df[["Date", "Open", "Close", "Volume"]].tail(10))

        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Close"], label="Päätöskurssi", color="blue")
        ax.set_xlabel("Päivämäärä")
        ax.set_ylabel("Kurssi")
        ax.set_title(f"{info.get('shortName', ticker)} - Kurssikehitys ({period})")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Virhe osakkeen haussa: {e}")
else:
    st.info("📝 Syötä osakkeen nimi tai ticker aloittaaksesi.")
