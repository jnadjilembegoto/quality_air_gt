import streamlit as st
from PIL import Image
from Image.image_link import image_dir


logo_path = image_dir("acc4.png")
logo = Image.open(logo_path)
def load_accueil():
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
    ####################



    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(logo, width=500)
    with col2:
        st.markdown("### 🌍La qualité de l’air en temps réel.")

        st.markdown('---')
        # Présentation des fonctionnalités clés
        #st.subheader("🔍 Fonctionnalités du tableau de bord :")
        st.markdown("""
        - 📊 **Visualisation des poluants** : Affichage graphique de l'historisque des différents polluants dans la ville de Yaoundé
        - 🤖 **Modèle de prédiction** : Évaluation de la qualité de l'air
        - 🧑‍💻 **Chat Air** : Pour une compréhension approfondie des notions et termes d'usage
        - ℹ️ **About us** : Une présentation des concepteurs de l'application
        """)
        st.markdown('---')
    st.markdown('---')
    ####################
    st.caption("Source : Données issues des capteurs installés par Stockholm Environment Institute.")
    # Footer
    st.markdown("---")
    #st.caption("Source : Données simulées pour la démonstration. En attente des données de Stockholm Environment Institute.")
