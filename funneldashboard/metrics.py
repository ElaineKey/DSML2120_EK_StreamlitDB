import pandas as pd

FUNNEL_STEPS = ["sessions", "product_views", "add_to_cart", "checkouts", "purchases"]

#step rates are based on conversion from the previous category, similar to app
#of ppl viewed product, what share added cart etc.
#pairs added to a dict, this is optimization from AI mentioned in final paragraph.
STEP_RATES = {
    "view_rate": ("product_views", "sessions"),
    "cart_rate": ("add_to_cart", "product_views"),
    "checkout_rate": ("checkouts", "add_to_cart"),
    "purchase_rate": ("purchases", "checkouts"),
}

def safe_div(num, den):
    return num / den if den else float("nan")


def kpis(df: pd.DataFrame) -> dict:
    t = df[FUNNEL_STEPS].sum()
    paid = df[df["traffic_source"] == "Paid Ads"]
    return {
#total visits and purchases converted to whole ints
        "sessions": int(t["sessions"]),
        "purchases": int(t["purchases"]),
#total conversion rate over all sessions
        "conversion_rate": safe_div(t["purchases"], t["sessions"]),
#of ppl who started check who completed purchase
        "checkout_completion": safe_div(t["purchases"], t["checkouts"]),
        "paid_cpa": safe_div(paid["ad_spend_usd"].sum(), paid["purchases"].sum()),
    }

def funnel_totals(df: pd.DataFrame, by: str = "device") -> pd.DataFrame:

#grouping rows by col, sum them
    return df.groupby(by)[FUNNEL_STEPS].sum()

def step_rates(df: pd.DataFrame, by: str = "device") -> pd.DataFrame:
    t = funnel_totals(df, by)
#creating table with row labels
    out = pd.DataFrame(index=t.index)
#adding rate cols one at a time
    for name, (num, den) in STEP_RATES.items():
        out[name] = t[num] / t[den]
    return out

#cost for advertising by device
def paid_cpa_by_device(df: pd.DataFrame) -> pd.DataFrame:
    paid = df[df["traffic_source"] == "Paid Ads"]
    g = paid.groupby("device")[["ad_spend_usd", "purchases", "sessions"]].sum()
    g["cost_per_purchase"] = g["ad_spend_usd"] / g["purchases"]
    g["cost_per_session"] = g["ad_spend_usd"] / g["sessions"]
    return g.reset_index()

#traffic conversion by source 
def conversion_by_source(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("traffic_source")[["sessions", "purchases"]].sum()
    g["conversion_rate"] = g["purchases"] / g["sessions"]
    g["session_share"] = g["sessions"] / g["sessions"].sum()
    return g.reset_index().sort_values("conversion_rate", ascending=False)

def over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    g = df.set_index("date")[["sessions", "purchases"]].resample(freq).sum()
    g["conversion_rate"] = g["purchases"] / g["sessions"]
    return g.reset_index()
