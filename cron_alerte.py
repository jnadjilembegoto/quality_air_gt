import pandas as pd
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

fom datas.data_link import data_dir
# === Charger les contacts depuis Excel ===
contacts = pd.read_excel(data_dir("contacts.xlsx"))  # assure-toi que le fichier est dans le bon dossier


# === 1. Charger les variables secrètes depuis .env ===
load_dotenv()

EMAIL_EXPEDITEUR = os.getenv("EMAIL_EXPEDITEUR")
MOT_DE_PASSE = os.getenv("EMAIL_PASSWORD")

# === 2. Charger les contacts ===
try:
    contacts = pd.read_excel("contacts.xlsx")
except FileNotFoundError:
    print("❌ Le fichier contacts.xlsx est introuvable.")
    exit()

# === 3. Simulation AQI / PM2.5 ===
pm25 = 138
niveau = "Bon" if pm25 <= 50 else "Modéré" if pm25 <= 100 else "Mauvais"

# === 4. Connexion au serveur SMTP ===
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)

        for _, row in contacts.iterrows():
            nom = row["Nom"]
            email = row["Email"]

            # === 5. Message personnalisé ===
            texte = f"""\
Bonjour {nom},

🧪 PM2.5 prévu aujourd’hui à Yaoundé : {pm25} µg/m³
💡 Niveau de qualité de l'air : {niveau}

Prenez les précautions nécessaires, surtout si vous êtes sensible ou asthmatique.

Cordialement,  
Équipe ISSEA – SEI
"""

            msg = MIMEText(texte)
            msg["Subject"] = f"Alerte qualité de l'air - PM2.5 : {pm25} µg/m³"
            msg["From"] = EMAIL_EXPEDITEUR
            msg["To"] = email

            server.sendmail(EMAIL_EXPEDITEUR, email, msg.as_string())
            print(f"✅ Email envoyé à {nom} ({email})")

except Exception as e:
    print(f"❌ Erreur lors de l’envoi des emails : {e}")

