import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from datas.data_link import data_dir
path = data_dir('base_finale_gt.xlsx')
def prev_load():
    data = pd.read_excel(path, sheet_name='CIDE_5m')
    
        # Fonction de mise en couleur AQI
    def color_aqi_transposed(val): 
        try:
            val = float(val)
        except:
            return ""
        
        if val <= 50:
            return "background-color: green; color: white"
        elif val <= 100:
            return "background-color: yellow; color: black"
        elif val <= 150:
            return "background-color: orange; color: white"
        elif val <= 200:
            return "background-color: red; color: white"
        elif val <= 300:
            return "background-color: purple; color: white"
        else:
            return "background-color: maroon; color: white"

    def color_pm25_aqi(val):
        try:
            val = float(val)
        except:
            return ""
        
        if val <= 12.0:
            return "background-color: green; color: white"         # Bon
        elif val <= 35.4:
            return "background-color: yellow; color: black"        # Modéré
        elif val <= 55.4:
            return "background-color: orange; color: white"        # Mauvais pour les groupes sensibles
        elif val <= 150.4:
            return "background-color: red; color: white"           # Mauvais
        elif val <= 250.4:
            return "background-color: purple; color: white"        # Très mauvais
        else:
            return "background-color: maroon; color: white"        # Dangereux

    # === INTERFACE ===

    prediction_aqi = 92.4
    niveau = "Bon" if prediction_aqi <= 50 else "Moyen" if prediction_aqi <= 100 else "Mauvais"
    
    

   
    # === Mise en forme via HTML englobant ===
    st.markdown("""
        <style>
            .encadre {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .conteneur-flex {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)
    now = datetime.datetime.now().strftime('%H:%M:%S')
   
    # Utilisation d'une DIV englobante
    st.markdown("""
        <div class="encadre">
            <div class="conteneur-flex">
                <div style="font-size: 28px; font-weight: bold;">🌫️ Prévision de la Qualité de l'air à Yaoundé</div>
                <div>
                    <p style="margin:0;"><strong>Prévision AQI (Aujourd'hui  {now})</strong></p>
                    <p style="font-size: 24px; color: #444; margin:0;">{val}</p>
                    <p style="color: #888; margin:0;">{niveau}</p>
                </div>
            </div>
        </div>
    """.format(val=f"{prediction_aqi:.1f}", niveau=niveau,now=now), unsafe_allow_html=True)
    with st.expander("ℹ️ Que savoir sur cette section?"):
        st.markdown("""
    Cette section vous permet de visualiser les données de qualité de l'air à Yaoundé.
    Vous pouvez explorer les tendances des différents polluants et leur impact sur la santé publique.
    """)

    col1, col2 = st.columns([2, 1])
    
    # Bloc principal
    with col1:
        st.subheader("Prévisions horaires du PM2.5 et de l'AQI")
        heures_disponibles = data["Hour"].unique().tolist()
        # ...existing code...
        # Créer deux sous-colonnes dans col2
        subcol1, subcol2 = st.columns([1, 1])
        # Insérer le selectbox dans la première sous-colonne
        heure_selectionnee = subcol1.selectbox(
            "Choisir une heure :", ["Toutes"] + heures_disponibles
        )
        
        jour_selectionne = subcol2.selectbox("Choisir un jour :",data["Jour"].unique().tolist())

        #df_transpose = data_horaire.set_index("Heure").T
        #styled_df = df_transpose.style.applymap(color_aqi_transposed)
        data_horaire=data[data["Jour"]==jour_selectionne]
        data_horaire = data_horaire[["PM2.5 (ug/m3)","AQI US", "Hour"]].groupby("Hour", as_index=False)[["PM2.5 (ug/m3)","AQI US"]].mean()
        df_horaire_filtrée = data_horaire if heure_selectionnee == "Toutes" else data_horaire[data_horaire["Hour"] == heure_selectionnee]
        df_transpose = df_horaire_filtrée.set_index("Hour").T
        #st.dataframe(df_transpose.style.applymap(color_aqi_transposed), use_container_width=True)

                # Transposer pour appliquer les styles correctement
        styled_df = (
            df_transpose.T
            .style
            .applymap(color_pm25_aqi, subset=["PM2.5 (ug/m3)"])
            .applymap(color_aqi_transposed, subset=["AQI US"])
            .format(precision=2)
        )

        # Affichage avec les couleurs via st.write
        st.write(styled_df)


    # Affichage Streamlit
        #st.dataframe(styled_df, use_container_width=True)
        with st.expander("ℹ️ Légende des niveaux AQI et PM2.5"):
            
            st.markdown("""

                            | Couleur   | AQI US     | PM2.5 (µg/m³)       | Description                           |
                            |-----------|------------|---------------------|----------------------------------------|
                            | 🟩 Vert   | 0 – 50     | 0.0 – 12.0          | Bonne qualité de l’air                 |
                            | 🟨 Jaune  | 51 – 100   | 12.1 – 35.4         | Qualité modérée                        |
                            | 🟧 Orange | 101 – 150  | 35.5 – 55.4         | Mauvaise pour les groupes sensibles   |
                            | 🟥 Rouge  | 151 – 200  | 55.5 – 150.4        | Mauvaise qualité de l’air              |
                            | 🟪 Violet | 201 – 300  | 150.5 – 250.4       | Très mauvaise qualité                  |
                            | 🟫 Marron | 301 – 500  | 250.5 – 500.4       | Dangereuse                             |
                            """)



        #st.dataframe(data_horaire.set_index("Heure").style.applymap(color_aqi, subset=["AQI"]), use_container_width=True)
        



    # Bloc latéral
    with col2:
        st.subheader("📆 Prévisions quotidiennes")
        #st.dataframe(donnees_jour.set_index("Jour"), use_container_width=True)
        # Appliquer couleur sur AQI quotidien
        #styled_jour = donnees_jour.set_index("Jour").style.applymap(color_aqi_transposed, subset=["AQI"])
        #st.dataframe(styled_jour, use_container_width=True)
        #donnees_jour=data[["PM10 (ug/m3)","Jour"]].copy()
        
        donnees_jour = data[["PM2.5 (ug/m3)","AQI US","Jour"]].groupby("Jour", as_index=False)[["PM2.5 (ug/m3)","AQI US"]].mean()
        # Filtre jour spécifique
        jours_disponibles = data["Jour"].unique().tolist()
        jour_selectionne = st.selectbox("Choisir un jour :", ["Tous"] + jours_disponibles)
        df_jour_filtré = donnees_jour if jour_selectionne == "Tous" else donnees_jour[donnees_jour["Jour"] == jour_selectionne]
        #styled_jour = df_jour_filtré.set_index("Jour").style.applymap(color_aqi_transposed, subset=["PM2.5 (ug/m3)","AQI US"])
        #st.dataframe(styled_jour, use_container_width=True)

        styled_jour = (
                        df_jour_filtré
                        .set_index("Jour")
                        .style
                        .applymap(color_pm25_aqi, subset=["PM2.5 (ug/m3)"])
                        .applymap(color_aqi_transposed, subset=["AQI US"])
                        .format(precision=2)
                    )

        st.write(styled_jour)


        
    today = datetime.date.today()
   
    st.subheader(f"Prévision horaire du particule (PM2.5) : {today.strftime('%d/%m/%Y')}")
        # Filtre heure spécifique
    heures_disponibles = data["Hour"].unique().tolist()
   # heure_selectionneeP = st.selectbox("Choisir une heure :", ["Toutes"] + heures_disponibles)
    data_horaire = data[["PM2.5 (ug/m3)", "Hour"]].groupby("Hour", as_index=False)[["PM2.5 (ug/m3)"]].mean()
    # Graphique dynamique avec Plotly
    fig = px.bar(
        data_horaire,
        x="Hour",
        y="PM2.5 (ug/m3)",
        color="PM2.5 (ug/m3)",
        color_continuous_scale=["green", "orange", "red", "purple"],
        #title="Prévision horaire de l'indice de qualité de l'air",
        labels={"AQI": "Indice AQI"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
       


    st.markdown("### 😷 Recommandations de santé")
    st.markdown("- Les groupes sensibles doivent éviter les activités de plein air.")
    st.markdown("- Fermez les fenêtres pour éviter l’air pollué.")
    st.markdown("- Utilisez un purificateur d’air si possible.")
    
