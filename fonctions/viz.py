import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

from datas.data_link import data_dir
path = data_dir('base_finale_gt.xlsx')


    
def viz_load():
    data = pd.read_excel(path, sheet_name='CIDE_5m')
    
    data["Datetime_start"] = pd.to_datetime(data["Datetime_start"])
   
    # Chargement des données (adaptez à votre source)
    now = datetime.datetime.now().strftime('%H:%M:%S')
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
                <div style="font-size: 28px; font-weight: bold;">🌍 Visualisation interactive de la qualité de l’air à Yaoundé</div>
                <div>
                    <p style="margin:0;"><strong>Heure de connexion : {now})</strong></p>
                </div>
            </div>
        </div>
    """.format(now=now), unsafe_allow_html=True)
    #st.title("🌍 Visualisation interactive de la qualité de l’air à Yaoundé")

    # ========= 1. Évolution temporelle =========
    with st.expander("📈 Comment évolue la pollution au fil du temps ?", expanded=True):
        st.caption("📌 Visualisez l'évolution journalière ou horaire des concentrations de polluants comme PM2.5, PM10, CO2, AQI US/CN...")

        polluants = ['PM2.5 (ug/m3)', 'PM10 (ug/m3)', 'PM1 (ug/m3)', 'CO2 (ppm)', 'AQI US', 'AQI CN']
        polluant_choisi = st.selectbox("Sélectionnez un polluant à visualiser :", polluants)

        fig = px.line(
            data,
            x="Datetime_start",
            y=polluant_choisi,
            title=f"Évolution temporelle de {polluant_choisi}",
            labels={"Datetime_start": "Date", polluant_choisi: polluant_choisi},
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========= 2. Influence des conditions météo =========
    with st.expander("🌡️ Les conditions météo influencent-elles la pollution ?", expanded=False):
        st.caption("📌 Explorez les relations entre température, humidité ou pression et la concentration en PM2.5 à l'aide de nuages de points.")

        xcol = st.selectbox("Variable météo :", ["Temperature (Celsius)", "Humidity (%)", "Pressure (pascal)"])
        fig = px.scatter(data, x=xcol, y="PM2.5 (ug/m3)", color="PM2.5 (ug/m3)",
                        title=f"Relation entre {xcol} et PM2.5", trendline="ols")
        st.plotly_chart(fig, use_container_width=True)

    # ========= 3. Périodes critiques de pollution =========
    with st.expander("🕒 Quand observe-t-on le plus de pollution ?", expanded=False):
        st.caption("📌 Comparez les niveaux de PM2.5 selon l'heure, le jour de la semaine ou le mois à l'aide de diagrammes en boîte.")

        time_type = st.radio("Regrouper par :", ["Hour", "Jour", "Month"], horizontal=True)
        fig = px.box(data, x=time_type, y="PM2.5 (ug/m3)", points="all",
                    title=f"Niveaux de PM2.5 par {time_type.lower()}")
        st.plotly_chart(fig, use_container_width=True)

    # ========= 4. Impact des saisons =========
    with st.expander("🌦️ Quel est l’impact des saisons sur la pollution ?", expanded=False):
        st.caption("📌 Observez comment la pollution (PM2.5) varie selon les saisons (saison sèche, saison des pluies...).")

        fig = px.violin(
            data,
            x="Saison",
            y="PM2.5 (ug/m3)",
            box=True,
            points="all",
            color="Saison",
            title="Distribution de PM2.5 selon les saisons",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========= 5. Relations entre les variables =========
    with st.expander("🔁 Quelles variables évoluent ensemble ?", expanded=False):
        st.caption("📌 Affichez une matrice de corrélation pour identifier les liens entre PM2.5, CO2, température, humidité, etc.")

        correlation_data = data[['PM2.5 (ug/m3)', 'PM10 (ug/m3)', 'PM1 (ug/m3)', 'CO2 (ppm)', 'AQI US', 'AQI CN',
                                'Temperature (Celsius)', 'Humidity (%)', 'Pressure (pascal)']].corr().round(2)
        
        fig = px.imshow(
            correlation_data,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title="Corrélations entre variables",
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)

 
