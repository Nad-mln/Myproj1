import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from pandas import read_csv
import pandas as pd
import seaborn as sns
from pandas.plotting import scatter_matrix
 
 
st.sidebar.title("Statistiques descriptives de Beans et Pods")
menu=st.sidebar.selectbox("Navigation",['Les données','Peek at the data','Statistiques','Corrélation','Visualisation','Analyse par canal et région','Conclusion'])
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

    st.header('Distribution de Robusta')
    figure,ax=plt.subplots()
    data['Robusta'].hist(bins=20, color='blue', edgecolor='black', ax=ax)
    ax.set_xlabel('Quantité de Robusta')
    ax.set_ylabel('Nombre de transactions')
    st.pyplot(figure)

elif menu=='Statistiques':
    st.header("Statistiques descriptives")
    st.write(data.describe())
    st.header('La Moyenne: ')
    st.write(data.select_dtypes(include=np.number).mean())

elif menu=='Corrélation': 
    st.header('La corrélation de Pearson')
    figure,ax=plt.subplots(figsize=(15,15))
    sns.heatmap(data.corr(method='pearson',numeric_only=True),annot=True,fmt='.2f',cmap='coolwarm',ax=ax)
    st.pyplot(figure)

elif menu=='Visualisation':
    st.header("Visualisation des données")
    st.subheader("Histogramme de la distribution de toutes les saveurs")
    data.hist(bins=20,figsize=(15,10),grid=True,layout=(3,3),color='blue')
    st.pyplot(plt.gcf())
 
    st.subheader("Histogramme de la distribution du Cappuccino")
    figure,ax=plt.subplots(figsize=(15,15))
    ax.hist(data['Cappuccino'], bins=20, color='orange', edgecolor='black')
    ax.set_xlabel('Quantité de Cappuccino')
    ax.set_ylabel('Nombre de consommateurs')
    st.pyplot(figure)

    st.subheader('Les Pairplots : préférences de café selon la région')
    sns.pairplot(data,hue='Region',vars=['Robusta','Arabica','Espresso','Lungo','Latte','Cappuccino'])
    st.pyplot(plt.gcf())

    st.subheader('Les valeurs aberrantes:')
    df=data.select_dtypes(include="number")
    resultat= []

    for col in df.columns:
        Q1 = np.percentile(df[col], 25)
        Q2 = np.percentile(df[col], 50) 
        Q3 = np.percentile(df[col], 75)
    
        IQR = Q3 - Q1
        born_inf = Q1 - 1.5 * IQR
        born_sup = Q3 + 1.5 * IQR
    
        nb_out_inf = np.sum(df[col] < born_inf)
        nb_out_sup = np.sum(df[col] > born_sup)
        nb_total = nb_out_inf + nb_out_sup
    
        resultat.append({
            'colonne': col,
            'Q1': Q1,
            'Q2 (médiane)': Q2,
            'Q3': Q3,
            'IQR': IQR,
            'borne_inf': born_inf,
            'borne_sup': born_sup,
            'nb_out_inf': nb_out_inf,
            'nb_out_sup': nb_out_sup,
            'Total_outliers': nb_total
        })
    st.dataframe(resultat)

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
    
    st.subheader("Récapitulatif")
    if canal_ventes['Online'] > canal_ventes['Store']:
        st.write(f"Le canal qui génère le plus de ventes est : Online")
    else:
        st.write(f"Le canal qui génère le plus de ventes est : Store")
    
    if region_ventes['South'] > region_ventes['North'] and region_ventes['South'] > region_ventes['Central']:
        st.write(f"La région qui génère le plus de ventes est : South")
    elif region_ventes['North'] > region_ventes['South'] and region_ventes['North'] > region_ventes['Central']:
        st.write(f"La région qui génère le plus de ventes est : North")
    else:
        st.write(f"La région qui génère le plus de ventes est : Central")

elif menu=='Conclusion':
    st.header("Conclusion et Recommandations")
    
    produits = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    canal_ventes = data.groupby('Channel')[produits].sum().sum(axis=1)
    region_ventes = data.groupby('Region')[produits].sum().sum(axis=1)
    ventes_produits = data[produits].sum()
    
    st.subheader("Résultats de l'analyse")
    
    st.write("L'analyse des données de Beans & Pods a permis d'identifier les points suivants :")
    
    if canal_ventes['Online'] > canal_ventes['Store']:
        st.write("- Le canal en ligne génère un volume de ventes supérieur au réseau de magasins physiques")
    else:
        st.write("- Le réseau de magasins physiques génère un volume de ventes supérieur au canal en ligne")
    
    if region_ventes['South'] > region_ventes['North'] and region_ventes['South'] > region_ventes['Central']:
        st.write("- La région Sud concentre la plus forte activité commerciale")
    elif region_ventes['North'] > region_ventes['South'] and region_ventes['North'] > region_ventes['Central']:
        st.write("- La région Nord concentre la plus forte activité commerciale")
    else:
        st.write("- La région Centre concentre la plus forte activité commerciale")
    
    meilleur_produit = ventes_produits.sort_values(ascending=False).index[0]
    st.write(f"Le produit {meilleur_produit} représente la meilleure performance de vente")
    
    st.subheader("Recommandations stratégiques")
    
    st.write("""
    Afin d'optimiser le retour sur investissement de la prochaine campagne marketing, il est recommandé de :
    
    - Concentrer les investissements sur le canal et la région les plus performants
    - Utiliser le produit star comme élément central de la communication
    - Adapter l'offre commerciale aux préférences observées dans chaque région
    """)
    
    st.subheader("Pistes d'amélioration des données")
    
    st.write("""
    Pour enrichir les futures analyses, il serait pertinent de collecter :
    
    - Prix unitaires des produits
    - Montant total du panier
    - Promotions ou réductions appliquées sur les produits
    - Age des clients
    - Situation professionnelle des clients
    - Fréquence d'achat des clients
             
    """)    

else:
    st.write('Menu en construction')