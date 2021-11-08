from time import time
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
import statsmodels.api as sm
import streamlit as st
import plotly.express as px
from utils.utils import timed, dfs, st, YEARS, merged_df


@timed
def timeseries_decomposition(df):
    
    # proceeding to TS decomposition using statsmodels api
    df['valeur_fonciere'].clip(upper=df['valeur_fonciere'].quantile(.9), inplace=True)
    time_serie = df.groupby('date_mutation').valeur_fonciere.median()
    time_serie.fillna(method="ffill", inplace=True)
    time_serie_date = time_serie.index
    decomposed_full = sm.tsa.seasonal_decompose(time_serie, period=60, extrapolate_trend='freq')


    # global attendance graph
    evo_global_graph = []

    evo_global_graph.append(
        go.Scatter(
        x = time_serie_date.tolist(),
        y = decomposed_full.observed.tolist(),
        mode = 'lines',
        name = 'Daily evolution of median prices',
        line=dict(color="#548CA8")
        )
    ) 

    evo_global_layout = dict(title = "Daily evolution of median prices",
                    xaxis = dict(title = 'Time'),
                    yaxis = dict(title = 'Median price'),
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )

    # global trend graph
    trend_graph = []

    trend_graph.append(
        go.Scatter(
        x = time_serie_date.tolist(),
        y = decomposed_full.trend.tolist(),
        mode = 'lines',
        name = 'Trend of median prices',
        line=dict(color="#edb139")
        )
    )

    trend_layout = dict(title = "Trend of median prices",
                    xaxis = dict(title = 'Time'),
                    yaxis = dict(title = 'Median price'),
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )

    # global seasonality graph
    seasonal_graph = []

    seasonal_graph.append(
        go.Scatter(
        x = time_serie_date.tolist(),
        y = decomposed_full.seasonal.tolist(),
        mode = 'lines',
        name = 'Seasonality of median prices',
        line=dict(color="#26992e")
        )
    )

    seasonal_layout = dict(title = "Seasonality of median prices",
                    xaxis = dict(title = 'Time'),
                    yaxis = dict(title = 'Median price'),
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )

    # global residual graph
    residual_graph = []

    residual_graph.append(
        go.Scatter(
        x = time_serie_date.tolist(),
        y = decomposed_full.resid.tolist(),
        mode = 'lines',
        name = 'Residuals of median prices',
        line=dict(color="#b50d0d")
        )
    )

    residual_layout = dict(title = "Residuals of median prices",
                    xaxis = dict(title = 'Time'),
                    yaxis = dict(title = 'Median price'),
                    paper_bgcolor="#F8F8F8",
                    margin=go.layout.Margin(
                            l=15, r=15, b=15, t=35  
                        )
                    )


    # append all charts
    figures = []
    figures.append(dict(data=evo_global_graph, layout=evo_global_layout))
    figures.append(dict(data=trend_graph, layout=trend_layout))
    figures.append(dict(data=seasonal_graph, layout=seasonal_layout))
    figures.append(dict(data=residual_graph, layout=residual_layout))

    return figures


def app():

    st.header("**Timeseries analysis of real estate prices between 2016 and 2021**")
    
    st.write("")
    
    areas = merged_df['code_departement'].drop_duplicates().sort_values()
    area_code = st.selectbox('Select your area:', areas, index=72)

    # FILTERING DATA BY HOUR SELECTED
    sampled = merged_df[merged_df['code_departement'] == area_code]
    sampled.sort_index(inplace=True)

    # contains in that order : evo, trend, season, residuals
    figures = timeseries_decomposition(sampled)
    st.write("")

    for fig in figures:
        st.write("")
        st.plotly_chart(fig)