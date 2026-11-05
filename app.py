import streamlit as st

st.set_page_config(page_title"Funnel Dashboard, layout="wide")

@st.cache_data
def get_data():
    return load_data()

df_all = get_data()

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
