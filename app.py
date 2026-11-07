import streamlit as st
import pandas as pd

st.set_page_config(page_title"Funnel Dashboard, layout="wide")

@st.cache_data
def load():
    return pd.read_csv("website_funnel.csv", parse_dates=["date"])

df = load()

# START SIDEBAR FILTERS ---

st.sidebar.header("Filters")
dates = st.sidebar.date_input("Date range", (df.date.min().date(), df.date.max().date()))
sources = st.sidebar.multiselect("Traffic source", df.traffic_source.unique(), df.traffic_source.unique())
devices = st.sidebar.multiselect("Device", df.device.unique(), df.device.unique())
freq = st.sidebar.radio("Time view", ["D", "W", "MS"], index=1, horizontal=True)

# If length of dates is less than two we stop,
if len(dates) < 2:
    st.stop()

# Filter pd through three conditions, if we have anything left we return it.
df = df[df.date.between(str(dates[0]), str(dates[1])) & df.traffic_source.isin(sources) & df.device.isin(devices)]
if df.empty:
    st.warning("No data for these filters.")
    st.stop()

# START KPIs ---

st.title("Key Performance Indicators")
t = df.sum(numeric_only=True)
paid = df[df.traffic_source == "Paid Ads"]

c = st.columns(5)
c[0].metric("Sessions", f"{t.sessions:,.0f}")
c[1].metric("Purchases", f"{t.purchases:,.0f}")
c[2].metric("Conversion rate", f"{t.purchases / t.sessions:.2%}")
c[3].metric("Checkout completion", f"{t.purchases / t.checkouts:.1%}")
c[4].metric("Paid cost / purchase", f"${paid.ad_spend_usd.sum() / paid.purchases.sum():.2f}" if len(paid) else "n/a")

# START CHARTS ---




#with st.sidebar:
#("How this app is organized (for students)"):
#    st.write(
#        """
#        - `app.py` is the entry point.
#        - Pages live in the `/pages` folder and auto-appear in the sidebar.
#        - Edit `pages/1_Bio.py` and `pages/2_Visualization.py` to complete the assignment.
#        """
#    )
#
#st.caption("Built with Streamlit • Class template")
