import streamlit as st
import pandas as pd

st.set_page_config(page_title"Funnel Dashboard, layout="wide")

@st.cache_data
def load():
    return pd.read_csv("website_funnel.csv", parse_dates=["date"])

df = load()

with st.sidebar:
("How this app is organized (for students)"):
    st.write(
        """
        - `app.py` is the entry point.
        - Pages live in the `/pages` folder and auto-appear in the sidebar.
        - Edit `pages/1_Bio.py` and `pages/2_Visualization.py` to complete the assignment.
        """
    )

st.caption("Built with Streamlit • Class template")
