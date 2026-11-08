"""Functions that turn tidy dataframes into Plotly figures."""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from metrics import FUNNEL_STEPS


def funnel_chart(totals):
    fig = go.Figure()
    for device, row in totals.iterrows():
        fig.add_trace(go.Funnel(name=device, y=FUNNEL_STEPS, x=row[FUNNEL_STEPS].tolist()))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), legend_title_text="Device")
    return fig

def step_conversion_chart(rates):
    long = rates.reset_index().melt(id_vars=rates.index.name, var_name="step", value_name="rate")
    
