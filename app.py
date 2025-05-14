import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
from PIL import Image
import numpy as np
from Image.image_link import image_dir

# === CONFIGURATION ===
st.set_page_config(page_title="Qualité de l'air à Yaoundé", layout="wide")

issea = Image.open(image_dir("logo_issea.png"))
sei = Image.open(image_dir("sei_logo.jpg"))
# === SIMULATION DES DONNEES ===
# (À remplacer par des appels API ou des fichiers réels)
date_actuelle = datetime.datetime.now()
horaires = pd.date_range(start=date_actuelle.replace(hour=23, minute=0), periods=13, freq="H")

data_horaire = pd.DataFrame({
    "Heure": horaires.strftime("%H:%M"),
    "PM2.5": [25, 160, 74, 65, 64, 125, 61, 59, 58, 56, 185, 56, 56]
})

jours = ["Aujourd’hui", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim.", "Lun."]
donnees_jour = pd.DataFrame({
    "Jour": jours,
    "PM2.5": [73, 61, 62, 63, 56, 69, 63]
})

# === SIDEBAR ===
st.sidebar.title("🔍 Période de prévision")



# Filtre jour spécifique
jours_disponibles = donnees_jour["Jour"].tolist()
jour_selectionne = st.sidebar.selectbox("Choisir un jour :", ["Tous"] + jours_disponibles)

# Filtre heure spécifique
heures_disponibles = data_horaire["Heure"].tolist()
heure_selectionnee = st.sidebar.selectbox("Choisir une heure :", ["Toutes"] + heures_disponibles)
st.sidebar.markdown("---")
st.sidebar.image(issea, caption="Institut Sous régional de Statistique et d'Economie Appliquée", use_container_width=True)
st.sidebar.image(sei, caption="Stockholm Environment Institute", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### À propos de nous")
st.sidebar.markdown("Cette application a été développée par deux ingénieurs statisticiens économistes de l'ISSEA dans le cadre de leur mémoire de GT.")
# Fonction de mise en couleur AQI
def color_aqi_transposed(val):
    try:
        val = float(val)
    except:
        return ""
    if val <= 50:
        return "background-color: green; color: white"
    elif val <= 100:
        return "background-color: orange; color: white"
    elif val <= 150:
        return "background-color: red; color: white"
    else:
        return "background-color: purple; color: white"




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

# Utilisation d'une DIV englobante
st.markdown("""
    <div class="encadre">
        <div class="conteneur-flex">
            <div style="font-size: 28px; font-weight: bold;">🌫️ Qualité de l'air à Yaoundé</div>
            <div>
                <p style="margin:0;"><strong>Prévision AQI (Demain 07h)</strong></p>
                <p style="font-size: 24px; color: #444; margin:0;">{val}</p>
                <p style="color: #888; margin:0;">{niveau}</p>
            </div>
        </div>
    </div>
""".format(val=f"{prediction_aqi:.1f}", niveau=niveau), unsafe_allow_html=True)


col1, col2 = st.columns([2, 1])

# Bloc principal
with col1:
    st.subheader("Prévisions horaires de l'AQI")
    
    #df_transpose = data_horaire.set_index("Heure").T
    #styled_df = df_transpose.style.applymap(color_aqi_transposed)
    df_horaire_filtrée = data_horaire if heure_selectionnee == "Toutes" else data_horaire[data_horaire["Heure"] == heure_selectionnee]
    df_transpose = df_horaire_filtrée.set_index("Heure").T
    st.dataframe(df_transpose.style.applymap(color_aqi_transposed), use_container_width=True)

# Affichage Streamlit
    #st.dataframe(styled_df, use_container_width=True)
    with st.expander("ℹ️ Légende des niveaux AQI"):
        st.markdown("""
    - 🟩 **Vert (0–50)** : Bon  
    - 🟧 **Orange (51–100)** : Modéré  
    - 🟥 **Rouge (101–150)** : Mauvais pour les groupes sensibles  
    - 🟪 **Violet (>150)** : Très mauvais
    """)

    #st.dataframe(data_horaire.set_index("Heure").style.applymap(color_aqi, subset=["AQI"]), use_container_width=True)
    



# Bloc latéral
with col2:
    st.subheader("📆 Prévisions quotidiennes")
    #st.dataframe(donnees_jour.set_index("Jour"), use_container_width=True)
    # Appliquer couleur sur AQI quotidien
    #styled_jour = donnees_jour.set_index("Jour").style.applymap(color_aqi_transposed, subset=["AQI"])
    #st.dataframe(styled_jour, use_container_width=True)
    df_jour_filtré = donnees_jour if jour_selectionne == "Tous" else donnees_jour[donnees_jour["Jour"] == jour_selectionne]
    styled_jour = df_jour_filtré.set_index("Jour").style.applymap(color_aqi_transposed, subset=["PM2.5"])
    st.dataframe(styled_jour, use_container_width=True)

    
col1g, col2g = st.columns([1, 1])
with col1g:
    st.subheader("Prévision horaire de qualité de l'air (PM2.5)")
    # Graphique dynamique avec Plotly
    fig = px.bar(
        data_horaire,
        x="Heure",
        y="PM2.5",
        color="PM2.5",
        color_continuous_scale=["green", "orange", "red", "purple"],
        #title="Prévision horaire de l'indice de qualité de l'air",
        labels={"AQI": "Indice AQI"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
with col2g:
    st.subheader("Prévision mensuelle de la qualité de l'air (PM2.5)")
    # Générer 31 jours de données pour mai
    dates_mois = pd.date_range(start="2024-05-01", end="2024-05-31")
    pm25_values = np.random.randint(30, 180, size=len(dates_mois))  # PM2.5 simulés

    # Créer le DataFrame
    donnees_mensuelles = pd.DataFrame({
        "Date": dates_mois,
        "PM2.5": pm25_values
    })

    fig_mois = px.bar(
    donnees_mensuelles,
    x="Date",
    y="PM2.5",
    color="PM2.5",
    color_continuous_scale=["green", "orange", "red", "purple"],
    #title="Prévision mensuelle de la qualité de l'air (PM2.5)",
    labels={"PM2.5": "Polluant PM2.5", "Date": "Jour"}
)
    fig_mois.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_mois, use_container_width=True)


st.markdown("### 😷 Recommandations de santé")
st.markdown("- Les groupes sensibles doivent éviter les activités de plein air.")
st.markdown("- Fermez les fenêtres pour éviter l’air pollué.")
st.markdown("- Utilisez un purificateur d’air si possible.")
   

# Footer
st.markdown("---")
st.caption("Source : Données simulées pour la démonstration. En attente des données de Stockholm Environment Institute.")
