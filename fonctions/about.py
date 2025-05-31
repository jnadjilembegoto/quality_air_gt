import streamlit as st
def about_us_page():
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
    st.markdown("""
        <div class="encadre">
            <div class="conteneur-flex">
                <div style="font-size: 28px; font-weight: bold;">🤝 Découvrez qui nous sommes et notre engagement pour un air plus sain à Yaoundé.</div>
            </div>
    """, unsafe_allow_html=True)
    st.markdown("Nous sommes une équipe d'ingénieurs statisticiens économistes passionnés par l'analyse des données et la qualité de l'air. Notre objectif est de fournir des outils interactifs et informatifs pour sensibiliser le public aux enjeux environnementaux.")
    