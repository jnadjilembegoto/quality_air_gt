import streamlit as st
from PIL import Image
from Image.image_link import image_dir
from fonctions.accueil import load_accueil
from fonctions.about import about_us_page
from fonctions.viz import viz_load
from fonctions.prev import prev_load
#from fonctions.ChatAir import chat_load
# === CONFIGURATION ===
st.set_page_config(page_title="Qualité de l'air à Yaoundé", layout="wide")

issea = Image.open(image_dir("logo_issea.png"))
sei = Image.open(image_dir("sei_logo.jpg"))
st.markdown("""
        <style>
            .custom-box {
                border: 3px solid #8B0000;  /* Rouge foncé */
                padding: 5px;
                width: 100%;
                margin: auto;
                border-radius: 12px;
                box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.2);
                background-color: #87CEEB; /*#fff5f5 Blanc rosé */
            }
            .title-text {
                text-align: center;
                font-size: 26px;
                font-weight: bold;
                color: #fff5f5; /* Rouge bordeaux */
                font-family: 'Arial', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <div class="custom-box">
        <h1 class="title-text">🌫️ Stat for SkyClear</h1>
    </div>
""", unsafe_allow_html=True)
    st.markdown("""
    <style>
        .thick-border {
            border: 4px solid #333; /* épaisseur gros, couleur noire */
            padding: 10px; /* padding intérieur */
            border-radius: 8px; /* coins arrondis si tu veux */
        }
    </style>
""", unsafe_allow_html=True)

    with st.container():
        choice = st.radio(
            "",
            ("🏠 Accueil", "📊 Visualisation", "🤖 Prévision", "🧑‍💻 Chat Air", "ℹ️ About Us")
        )
    

    st.markdown('---')
    st.image(issea, caption="Institut Sous régional de Statistique et d'Economie Appliquée", use_container_width=True)
    st.image(sei, caption="Stockholm Environment Institute", use_container_width=True)
    st.markdown("---")                                                                                                  
####################
if choice == "🏠 Accueil":
    load_accueil()
elif choice=='📊 Visualisation':
    viz_load()
elif choice == "🤖 Prévision":
    #st.markdown("Cette fonctionnalité est en cours de développement. Restez à l'écoute pour les mises à jour !")
    prev_load()
elif choice == "🧑‍💻 Chat Air":
    st.markdown("Cette fonctionnalité est en cours de développement. Restez à l'écoute pour les mises à jour !")
    #chat_load()
else:
    about_us_page()
