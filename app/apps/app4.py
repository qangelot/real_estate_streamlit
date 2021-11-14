import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.utils import timed, dfs, st, YEARS


# CREATING FUNCTION FOR MAPS
@timed
def map(df, lat, lon, midpoint, col):

    fig = px.density_mapbox(df, lat=lat, lon=lon, z=col, hover_data=['surface_reelle_bati', 'nombre_pieces_principales'], 
                        radius=10, center=dict(lat=midpoint[0], lon=midpoint[1]), zoom=9,
                        width=800, height=700, mapbox_style="stamen-terrain")

    fig.update_layout(
        paper_bgcolor= "#F8F8F8",
        margin=dict(
                l=15, r=15, b=35, t=35 
        )
    )
    fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig)


def app():


    year_choice = st.sidebar.selectbox('Select year:', YEARS)

    # FILTERING DATA BY YEARS
    df = dfs[year_choice]

    st.header("**Geospatial analysis**")
    
    st.write("")

    areas = df['code_departement'].drop_duplicates().sort_values()
    area_code = st.selectbox('Select your area:', areas)

    # FILTERING DATA BY HOUR SELECTED
    sampled = df[df['code_departement'] == area_code]

    # sampling only part of the data for computation speed
    sampled.dropna(subset=['valeur_fonciere', 'surface_reelle_bati', 'nombre_pieces_principales', 'latitude', 'longitude'], inplace=True)
    
    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    midpoint = [np.average(sampled["latitude"]), np.average(sampled["longitude"])]  

    st.write("")

    st.subheader(f"Geospatial analysis of real estate transactions in {area_code}")
    st.write("")

    st.write("Please do note that some data is not shown if the amount of transactions is below a certain threshold.")

    map(sampled, 'latitude', 'longitude', midpoint, 'valeur_fonciere')
    st.markdown("_Color intensity correlate positively with valeur_fonciere._")