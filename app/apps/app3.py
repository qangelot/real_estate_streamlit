import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import timed, dfs, st, YEARS
 


@timed
def plot_dist(df, col1, color):
    # fig = px.box(df, x=col1, y="valeur_fonciere")
    # fig.update_yaxes(range=(0, df["valeur_fonciere"].quantile(.95)))

    fig_graph = (
        go.Box(
        x = df[col1],
        y = df["valeur_fonciere"],
        name = col1,
        boxmean=True,
        notched=True,
        line=dict(color=color)
        )
    )

    fig_layout = dict(title = f"{col1} vs valeur_fonciere",
                    xaxis = dict(title = col1),
                    yaxis = dict(title = 'valeur_fonciere'),
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )

    fig = dict(data=fig_graph, layout=fig_layout)

    st.plotly_chart(fig)
    

def app(): 


    year_choice = st.sidebar.selectbox('Select year:', YEARS)

    # FILTERING DATA BY YEARS
    df = dfs[year_choice]

    st.header("**Multivariate analysis II**")

    st.write("")


    ##################################filtered by area################################

    st.write("")

    st.subheader("**Filtered by geographic areas**")
    st.write("")

    areas = df['code_departement'].drop_duplicates().sort_values()
    area_choice = st.selectbox('Select your area:', areas)

    # FILTERING DATA BY AREAS
    sampled = df.loc[(df['code_departement'] == area_choice)]
    sampled = sampled.loc[(sampled['valeur_fonciere'] < sampled["valeur_fonciere"].quantile(.95))]


    discrete = ['nombre_pieces_principales', 'mois_mutation', 'type_local']
    colors = ['#9960d6', '#26992e', '#b50d0d']
    for col, color in zip(discrete, colors):
        st.write("")
        plot_dist(sampled, col, color)  



    