import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import timed, dfs, st, YEARS
 

@timed
def discrete_distri(df, col):
    fig = go.Figure(data=[go.Pie(labels=df[col], values=df[col], hole=.25)], layout=dict(title = f"Distribution of nombre_pieces_principales", paper_bgcolor="#F8F8F8"))
    
    st.plotly_chart(fig)


@timed
def plot_dist(df, col, color):

    fig_graph = (
        go.Histogram(
        x = df[col],
        y = df["valeur_fonciere"],
        name = col,
        marker_color=color            )
    )

    fig_layout = dict(title = f"Distribution of {col}",
                    xaxis = dict(title = col, range=[0, df[col].quantile(.95)]),
                    yaxis = dict(title = 'volume'),autosize=False,
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )
    
    fig = dict(data=fig_graph, layout=fig_layout)

    st.plotly_chart(fig)
    

def app(): 

    year_choice = st.sidebar.selectbox('Select year:', YEARS)
    print(year_choice)
    # FILTERING DATA BY YEARS
    df = dfs[year_choice]

    st.header("**Univariate analysis**")

    st.write("")

    st.subheader("**Continuous variables**")

    continuous = ['valeur_fonciere', 'surface_reelle_bati', 'surface_terrain']
    colors = ['#9960d6', '#26992e', '#b50d0d']
    for col, color in zip(continuous, colors):
        st.write("")
        plot_dist(df, col, color)  

    st.write("")

    st.subheader("**Discrete variables**")

    discrete_distri(df, 'nombre_pieces_principales')  

    