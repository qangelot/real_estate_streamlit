import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import timed, data20, st
 

def app(): 

    st.header("**Univariate analysis**")

    st.write("")

    st.subheader("**Continuous variables**")
    

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
                        yaxis = dict(title = 'volume'),
                        )

        fig = dict(data=fig_graph, layout=fig_layout)

        st.plotly_chart(fig)


    continuous = ['valeur_fonciere', 'surface_reelle_bati', 'surface_terrain']
    colors = ['#9960d6', '#26992e', '#b50d0d']
    for col, color in zip(continuous, colors):
        plot_dist(data20, col, color)  

    st.write("")

    st.subheader("**Discrete variables**")

    @timed
    def discrete_distri(df, col):
        fig = go.Figure(data=[go.Pie(labels=df[col], values=df[col], hole=.25)])
        st.plotly_chart(fig)

    st.write(f"**Distribution of nombre_pieces_principales**")
    discrete_distri(data20, 'nombre_pieces_principales')  

    