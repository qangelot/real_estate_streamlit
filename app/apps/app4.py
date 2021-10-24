from utils.utils import timed, data20, st
import numpy as np
import folium
from streamlit_folium import folium_static
import pandas as pd


# CREATING FUNCTION FOR MAPS
@timed
def map(data, midpoint):

    map_osm = folium.Map(location=midpoint, zoom_start=5)
    data.apply(lambda row : folium.CircleMarker(location=[row["latitude"], row["longitude"]], 
                                              radius=10, fill_color=row['valeur_fonciere_q5'])
                                             .add_to(map_osm), axis=1)
    folium_static(map_osm)


def app():

    st.write("")

    st.header("**Geospatial analysis**")
    
    st.write("")

    # sampling only part of the data for computation speed
    sampled = data20.sample(frac =.99)
    sampled.dropna(inplace=True)
    
    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    midpoint = [np.average(sampled["latitude"]), np.average(sampled["longitude"])]  

    sampled['valeur_fonciere_q5'] = pd.qcut(sampled['valeur_fonciere'], 5, labels=False)


    st.subheader("Geospatial analysis of major real estate transactions in France in 2020")
    st.write("Please do note that this is a macro analysis and some data isn't shown if the amount of transactions is below a certain threshold.")
    st.write("")
    map(sampled, midpoint)
