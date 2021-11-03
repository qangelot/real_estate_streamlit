from apps import app1, app2, app3, app4, home
import streamlit as st
from multiapp import MultiApp


# add all apps
app = MultiApp()

app.add_app("Home", home.app)
app.add_app("Univariate analysis", app1.app)
app.add_app("Multivariate analysis I", app2.app)
app.add_app("Multivariate analysis II", app3.app)
app.add_app("Geospatial analysis", app4.app)

st.markdown(
    """
<style>

section.main.css-1v3fvcr.eknhn3m1 {
    background-color: 	#F8F8F8		;
}

</style>
""",
    unsafe_allow_html=True,
)


# The main app
app.run()