import streamlit as st
import time
import streamlit.components.v1 as components


def app():

    # LAYING OUT THE TOP SECTION OF THE APP

    components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <style> 
            body{
                background-color: 	#F8F8F8	;
            }
        </style>
        <div class="alert alert-success text-center " >
        Congratulations! Real Estate Analysis has been performed successfully 🎯 
        </div> <br>
        <br>
        <div class="card mx-auto" style="width: 50rem;">
        <img class="card-img-top" src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1073&q=80" alt="Card image cap">
        <div class="card-body">
            <h5 class="card-title">Analysis of Real Estate in France</h5>
            <p class="card-text">Examining Real Estate using different vizualisation techniques. By using the slider on the left you can view different slices of time and explore different trends.</p>
            <a href="https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/#_" class="btn btn-primary">Source dataset can be found here.</a>
        </div>
        </div>
        """,
        height=925
    )
    
    st.write("")
    st.subheader("Overview of the real estate market in France in 2021:") 
    st.video("https://www.youtube.com/watch?v=mIYLKgq8EsE&ab_channel=FigaroImmobilier")


    
