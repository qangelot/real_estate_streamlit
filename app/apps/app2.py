import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import timed, dfs, st, YEARS


@timed
def plot_dist(df):

    # création de sous-ensembles has_lot / no_lot
    has_lot = df[df['nombre_lots'] == 1]
    no_lot = df[df['nombre_lots'] == 0]

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=has_lot['valeur_fonciere'], 
        name="has_lot"))
    fig.add_trace(go.Histogram(x=no_lot['valeur_fonciere'], 
        name="no_lot"))
    # Overlay both histograms
    fig.update_layout(barmode='overlay', paper_bgcolor="#F8F8F8", 
                    margin=dict(
                        l=15, r=15, b=15, t=35
                        ), 
                    legend=dict(
                        orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1
                        )
                    )    
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    fig.update_xaxes(range=(0, no_lot['valeur_fonciere'].quantile(.95)))
    st.plotly_chart(fig)


@timed
def scatter(df, col, xmin=0):
    fig = px.scatter(df, x=col, y='valeur_fonciere', trendline="ols", 
        trendline_scope="overall",
        trendline_color_override="red")
    fig.update_layout(barmode='overlay',paper_bgcolor="#F8F8F8", margin=dict(
            l=15, r=15, b=15, t=35 
        ), legend=dict(yanchor="top",
            y=0.99, xanchor="left", x=0.01))
    fig.update_traces(opacity=0.5)
    fig.update_xaxes(range=(xmin, df[col].quantile(.95)))
    fig.update_yaxes(range=(0, df['valeur_fonciere'].quantile(.95)))

    st.plotly_chart(fig)


def app():


    year_choice = st.sidebar.selectbox('Select year:', YEARS)

    # FILTERING DATA BY YEARS
    df = dfs[year_choice]

    st.write("")

    st.header("**Multivariate analysis I**")

    st.write("")

    st.write("**Distributions of valeur_fonciere relatives to the presence of a lot or not**")
    plot_dist(df)
    
    st.write("")


    ##################################filtered by area################################

    st.write("")

    st.subheader("**Filtered by geographic areas**")

    st.write("")

    areas = df['code_departement'].drop_duplicates().sort_values()
    area_choice = st.selectbox('Select your area:', areas)

    # FILTERING DATA BY AREAS
    sampled = df.loc[(df['code_departement'] == area_choice)]

    st.write("")
    st.write("")
    st.write("")

    st.write("**Surface réelle and valeur_fonciere**")
    scatter(sampled, 'surface_reelle_bati')
    st.write("")
    st.write("")

    st.write("**Surface du terrain and valeur_fonciere**")
    scatter(sampled, 'surface_terrain')

