import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from pandas import read_csv
import pandas as pd
import seaborn as sns
from pandas.plotting import scatter_matrix
 
 
st.sidebar.title("Statistiques descriptives de Beans et Pods")
menu=st.sidebar.selectbox("Navigation",['Les données','Peek at the data','Statistiques','Corrélation','Visualisation','Conclusion'])
st.markdown(
    """
    <div style='text-align: center;'>
    <h1>Statistiques descriptives de Beans et Pods</h1> 
 
    </div>
    """,unsafe_allow_html=True
    )