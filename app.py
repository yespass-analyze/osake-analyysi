import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1) Data­lataus ja puhdistus
# ------------------------------
@st.cache_data
def lataa_data():
    df = pd.read_csv("nokia.csv", dtype=str)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    for col in ["Open","High","Low","Close","Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = lataa_data()
if df.empty:
    st.error("🛑 Data kelvottomassa kunnossa – tarkista `nokia.csv`.")
    st.stop()

# ------------------------------
# 2) Aikavälin valinta
# ------------------------------
period_map = {
    "1pv":   1,
    "1kk":  30,
    "3kk":  90,
    "6kk": 180,
    "12kk":365,
    "36kk":1095,
    "60kk":1825
}
valinta = st.selectbox(
    "Valitse aikaväli:",
    options=list(period_map.keys()),
    index=list(period_map.keys()).index("3kk")
)
days      = period_map[valinta]
last_date = df.index.max()
start_dt  = last_date - pd.Timedelta(days=days)
df_sel    = df[df.index >= start_dt]

# ------------------------------
# 3) Piirto-funktiot (ihan tässä)
# ------------------------------
def piirra_graafi(df, sarake, otsikko, signal_col=None):
    fig, ax = plt.subplots()
    ax.plot(df.index, df[sarake], label=sarake, color="blue")
    if signal_col in df.columns:
        buys  = df[df[signal_col]=="BUY"]
        sells = df[df[signal_col]=="SELL"]
        ax.scatter(buys.index,  buys[sarake],  marker="^", c="green", s=80, label="BUY")
        ax.scatter(sells.index, sells[sarake], marker="v", c="red",   s=80, label="SELL")
    ax.set_title(otsikko); ax.set_xlabel("Päivämäärä"); ax.set_ylabel("Arvo")
    ax.grid(True); ax.legend()
    return fig

def piirra_tunnusluvut():
    tunnus = {"P/E":15.2,"P/B":1.8,"ROE":12.5,"Debt/Equity":0.45}
    fig, ax = plt.subplots()
    ax.bar(tunnus.keys(), tunnus.values(), color="skyblue")
    ax.set_title("Nokian tunnusluvut"); ax.set_ylabel("Arvo")
    ax.set_ylim(0, max(tunnus.values())*1.2)
    for i,v in enumerate(tunnus.values()):
        ax.text(i, v+0.1, f"{v:.2f}", ha="center")
    return fig

def plot_trendlines(df):
    x = np.arange(len(df)); y = df["Close"].values
    coeff = np.polyfit(x, y, 1)
    trend = np.poly1d(coeff)(x)
    sigma = np.std(y - trend)
    ma5  = df["Close"].rolling(5).mean()
    ma20 = df["Close"].rolling(20).mean()

    fig, ax = plt.subplots()
    ax.plot(df.index,       y,     label="Close", color="green")
    ax.plot(df.index,       trend, "--", label="Trend", color="red")
    ax.fill_between(df.index, trend-sigma, trend+sigma,
                    color="red", alpha=0.1, label="Kanava ±1σ")
    ax.plot(df.index, ma5,  label="MA5",  color="blue",   lw=1)
    ax.plot(df.index, ma20, label="MA20", color="orange", lw=1)

    total = (trend[-1]-trend[0])/trend[0]*100
    ax.text(0.02,0.95, f"Slope {coeff[0]:.4f} ({total:.2f}%)",
            transform=ax.transAxes, va="top")
    ax.set_title("Trendiviiva ja kanavat"); ax.set_xlabel("Päivämäärä"); ax.set_ylabel("Close hinta")
    ax.grid(True); ax.legend()
    return fig

def arvioi_ostosuositus(df):
    close = df["Close"]
    pct   = (close.iloc[-1]-close.iloc[0])/close.iloc[0]*100
    ma5   = close.rolling(5).mean().iloc[-1]
    ma20  = close.rolling(20).mean().iloc[-1]
    ma_sig = "Bullish MA" if ma5>ma20 else "Bearish MA" if ma5<ma20 else "Neutral MA"

    if pct>2 and ma5>ma20: rec="Vahva osta"
    elif pct>0 and ma5>ma20: rec="Osta"
    elif pct<-2 and ma5<ma20: rec="Vahva myy"
    elif pct<0 and ma5<ma20: rec="Myy"
    else: rec="Pidä"

    return f"Hinta {pct:.2f}% → {rec} ({ma_sig})"

# ------------------------------
# 4) Streamlit-UI
# ------------------------------
st.title("📊 Nokian osakeanalyysi")

st.subheader("📈 Kurssi ja signaalit")
st.pyplot(piirra_graafi(df_sel, "Close", f"Nokia – Close", signal_col="Signal"))

st.subheader("💡 Suositus")
st.markdown(f"**{arvioi_ostosuositus(df_sel)}**")

st.subheader("📊 Tunnusluvut")
st.pyplot(piirra_tunnusluvut())

st.subheader("📉 Trendiviiva & kanavat")
st.pyplot(plot_trendlines(df_sel))

with st.expander("📄 Näytä raakadata"):
    st.dataframe(df_sel)
