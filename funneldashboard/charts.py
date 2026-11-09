"""Functions that turn tidy dataframes into Plotly figures."""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from metrics import FUNNEL_STEPS


#Funnel by device
def funnel_chart(totals):
    fig = go.Figure()
    for device, row in totals.iterrows():
        fig.add_trace(go.Funnel(name=device, y=FUNNEL_STEPS, x=row[FUNNEL_STEPS].tolist()))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), legend_title_text="Device")
    return fig

#conversion chart
def step_conversion_chart(rates):
#shaping table from wide to long
    long = rates.reset_index().melt(id_vars=rates.index.name, var_name="step", value_name="rate")
#draw chart conversion rate sets the bar height
    fig = px.bar(long, x="step", y="rate", color=rates.index.name, barmode="group")
    fig.update_yaxes(tickformat=".0%", title=None)
    fig.update_xaxes(title=None)
    return fig

#device x cost per purchase (cpp)
def cpa_chart(cpa):
    fig = px.bar(cpa, x="device", y="cost_per_purchase", text_auto="$.2f")
    fig.update_yaxes(title="Cost per purchase (USD)")
    return fig

#traffic source by conversion rate
def source_chart(src):
    fig = px.bar(src, x="conversion_rate", y="traffic_source", orientation="h",
                 hover_data={"session_share": ":.1%", "sessions": True})
    fig.update_xaxes(tickformat=".1%", title="Conversion rate")
    fig.update_yaxes(title=None, categoryorder="total ascending")
    return fig

#time chart as total
def time_chart(ts):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    #adding both lines to chart
    fig.add_trace(go.Scatter(x=ts["date"], y=ts["sessions"], name="Sessions"), secondary_y=False)
    fig.add_trace(go.Scatter(x=ts["date"], y=ts["conversion_rate"], name="Conversion rate"), secondary_y=True)

    #display conversion rate with tick format set as %
    fig.update_yaxes(title_text="Sessions", secondary_y=False)
    fig.update_yaxes(title_text="Conversion rate", tickformat=".1%", secondary_y=True)
    return fig
