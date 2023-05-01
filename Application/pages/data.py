# Import des librairies.
from librairie import background
import pymysql
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from bdd_2_tables import delete_content_tables

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')


def page_bdd():
    
    st.title("Notre base de données")
    st.subheader("Table de prédictions")
    
    # affichage du background + connexion à la base
    background(url="https://wallpaper.dog/large/10707630.jpg")
    table_images=pd.read_sql_query("SELECT * FROM images ", conn)
    table_predictions=pd.read_sql_query("SELECT * FROM predictions ", conn)
    data=False
    
    # Si la table est vide, on envoie un message d'erreur.
    if table_images.empty or  table_predictions.empty:
        st.error("Base de données vide !")
    else:
        df_final = table_predictions.merge(table_images, left_on='image_id', right_on='id')
        df_final = df_final.drop(["id_x", "id_y","image_id"], axis=1)
        st.write(df_final.head())
        data=True
        
    if st.button("Supprimer les données"):
        delete_content_tables()
    
    # Affichage du nombre d'occurrences de chaque valeur
    st.title(f"Exploration des Prédictions")
    if data:
        
        # Graphique 1
        st.subheader('Les Prédictions réaliser')
        sns.set_style('dark')
        fig, ax = plt.subplots()  # créer une figure et un axe
        sns.countplot(x='y_pred', data=df_final, ax=ax)  # tracer le graphique sur l'axe
        plt.xlabel("Les cibles prédites")
        plt.ylabel("Compte des cibles prédites")
        
        fig.savefig('countplot.png')  
        st.image('countplot.png')  

        # Graphique 2
        # ...
    
        
    else:
        st.error("Visualisation non disponible.")
        
page_bdd()


