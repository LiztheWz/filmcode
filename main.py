import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(['Genre', 
                                                                'IMDb Rating', 
                                                                'Runtime', 
                                                                'Director', 
                                                                'Actors', 
                                                                'Writers', 
                                                                'Producers',
                                                                'Distributor',
                                                                'Box Office'])


with tab1:
    st.write('Genre')

with tab2:
    st.write('IMDb Rating')

with tab3:
    st.write('Runtime')

with tab4:
    st.write('Directors')

with tab5:
    st.write('Actors')

with tab6:
    st.write('Writers')

with tab7:
    st.write('Producers')

with tab8:
    st.write('Distributor')

with tab9:
    st.write('Box Office')

