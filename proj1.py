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

chemin='BeansDataSet.csv'
col=['Channel','Region','Robusta','Arabica','Espresso','Lungo','Latte','Cappuccino']
ligne=[f'consommateur_{x}' for x in range(1, 441)]
data= read_csv(chemin)
data.index=ligne

if menu=='Les données':
    st.write("Voici les données de Beans & Pods:")
    st.dataframe(data)

elif menu=='Peek at the data':
    st.header("Aperçu des données")
    st.subheader("Affichage des premières et dernières lignes du dataset 'Beans & Pods'")
    data.shape
    st.write('Le nombre de consommateurs est de :',data.shape[0])
    st.write('Le nombre de types saveurs est de :',data.shape[1])

    st.header('Distribution des ventes de Robusta')
    figure,ax=plt.subplots()
    data['Robusta'].hist(bins=20, color='blue', edgecolor='black', ax=ax)
    ax.set_xlabel('Quantité de Robusta')
    ax.set_ylabel('Nombre de transactions')
    st.pyplot(figure)

elif menu=='Analyse par canal et région':
    st.header("Analyse des ventes par Canal et par Région")
    produits = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    st.subheader("Ventes par Canal") 
    canal_ventes = data.groupby('Channel')[produits].sum().sum(axis=1)
    st.write(canal_ventes)
    
    figure,ax=plt.subplots()
    canal_ventes.plot(kind='bar',color=['blue','green'],ax=ax)
    ax.set_xlabel('Canal')
    ax.set_ylabel('Ventes totales')
    st.pyplot(figure)
    
    
    st.subheader("Ventes par Région")
    region_ventes = data.groupby('Region')[produits].sum().sum(axis=1)
    st.write(region_ventes)
    figure,ax=plt.subplots()
    region_ventes.plot(kind='bar',color=['orange','red','purple'],ax=ax)
    ax.set_xlabel('Région')
    ax.set_ylabel('Ventes totales')
    st.pyplot(figure)
    
    
    st.subheader("Ventes par Canal et Région")
    croise_ventes = data.groupby(['Channel','Region'])[produits].sum().sum(axis=1)
    st.write(croise_ventes)
    figure,ax=plt.subplots(figsize=(10,6))
    croise_ventes.unstack().plot(kind='bar',ax=ax)
    ax.set_xlabel('Canal')
    ax.set_ylabel('Ventes totales')
    st.pyplot(figure)
    

else:
    st.write('Chargement en cours...')