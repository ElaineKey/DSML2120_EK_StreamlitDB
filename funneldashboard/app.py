from pathlib import Path

import pandas as pd
import streamlit as st

#fix using Path for running out of the cloud service.
st.set_page_config(page_title="Funnel Dashboard", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "website_funnel.csv"

# @st.load requirement for loading the csv available in the repoistory.
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


df = load_data()


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

#add all numeric cols,
#data frame containing all paid ads
t = df.sum(numeric_only=True)
paid = df[df.traffic_source == "Paid Ads"]

#creating cols 'c' for all key performance indicators.
c = st.columns(5)
c[0].metric("Sessions", f"{t.sessions:,.0f}")
c[1].metric("Purchases", f"{t.purchases:,.0f}")
#calculating KPI values 
c[2].metric("Conversion rate", f"{t.purchases / t.sessions:.2%}")
c[3].metric("Checkout completion", f"{t.purchases / t.checkouts:.1%}")
#total ad spending, total purchases from paid ads, only if the user actually converted as a sale.
#ai tool was used to help make this line-
c[4].metric("Paid cost / purchase", f"${paid.ad_spend_usd.sum() / paid.purchases.sum():.2f}" if len(paid) else "n/a")


# START CHARTS ---


#funnel conversion table by device type:
#device aggregation, groups the df by device col and sums the funnel counts
by_dev = df.groupby("device")[["sessions", "product_views", "add_to_cart", "checkouts", "purchases"]].sum()

#uses the bydev aggregate made above, and shows the share of customers from the previous that add to the next

#1 share sesions that find a product page
#2 share product views that add cart
#3 number of ads to cart that start checkout
#4 number of checkout starts that become purchases
rates = pd.DataFrame({
    "1 view": by_dev.product_views / by_dev.sessions,
    "2 cart": by_dev.add_to_cart / by_dev.product_views,
    "3 checkout": by_dev.checkouts / by_dev.add_to_cart,
    "4 purchase": by_dev.purchases / by_dev.checkouts,
})

#total by traffic source
by_src = df.groupby("traffic_source")[["sessions", "purchases"]].sum()
#paid spend and purchases by device
p = paid.groupby("device")[["ad_spend_usd", "purchases"]].sum()
#only keeping sessions and purchases cols, indexed by period
ts = df.set_index("date")[["sessions", "purchases"]].resample(freq).sum()

#funnel by device
left, right = st.columns(2)
left.subheader("Funnel by device")
left.bar_chart(by_dev.T.set_axis(["(1) sessions", "(2) views", "(3) cart", "(4) checkout", "(5) purchase"]))
right.subheader("Step conversion by device")
right.bar_chart(rates.T)

#CPP by device
left, right = st.columns(2)
left.subheader("Paid cost per purchase by device")
left.bar_chart(p.ad_spend_usd / p.purchases)
right.subheader("Conversion by traffic source")
right.bar_chart(by_src.purchases / by_src.sessions, horizontal=True)

#sessions total (over time)
left, right = st.columns(2)
left.subheader("Sessions over time")
left.line_chart(ts.sessions)
right.subheader("Conversion rate over time")
right.line_chart(ts.purchases / ts.sessions)

