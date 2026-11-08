from pathlib import Path

import pandas as pd
import streamlit as st

#fix using Path for running out of the cloud service.
st.set_page_config(page_title="Funnel Dashboard", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "website_funnel.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


df_all = load_data()

#this was originally planned to be read from a seperate file
#its now implemented to be inline for simplicity and I hate doing the seperate file so.
#@st.cache_data
#def load():
#    return pd.read_csv("website_funnel.csv", parse_dates=["date"])
#
#df = load()

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

by_dev = df.groupby("device")[["sessions", "product_views", "add_to_cart", "checkouts", "purchases"]].sum()
rates = pd.DataFrame({
    "1 view": by_dev.product_views / by_dev.sessions,
    "2 cart": by_dev.add_to_cart / by_dev.product_views,
    "3 checkout": by_dev.checkouts / by_dev.add_to_cart,
    "4 checkout": by_dev.purchases / by_dev.checkouts,
})

by_src = df.groupby("traffic_source")[["sessions", "purchases"]].sum()
p = paid.groupby("device")[["ad_spend_usd", "purchases"]].sum()
ts = df.set_index("date")[["sessions", "purchases"]].resample(freq).sum()

left, right = st.columns(2)
left.subheader("Funnel by device")
left.bar_chart(by_dev.T.set_axis(["1 sessions", "2 views", "3 cart", "4 checkout", "5 purchase"]))
right.subheader("Step conversion by device")
right.bar_chart(rates.T)

left, right = st.columns(2)
left.subheader("Paid cost per purchase by device")
left.bar_chart(p.ad_spend_usd / p.purchases)
right.subheader("Conversion by traffic source")
right.bar_chart(by_src.purchases / by_src.sessions, horizontal=True)

left, right = st.columns(2)
left.subheader("Sessions over time")
left.line_chart(ts.sessions)
right.subheader("Conversion rate over time")
right.line_chart(ts.purchases / ts.sessions)


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
