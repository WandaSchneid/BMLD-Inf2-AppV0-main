import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_Notenrechner")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame()
    )

page = "Startseite"

# --- Startseite ---
if page == "Startseite":
    st.title("📚 Notenrechner App")
    st.write("""
    Willkommen zum Notenrechner für das 2. Semester!  
    Hier kannst du deine Noten eingeben und deinen gewichteten Notendurchschnitt berechnen.
    
    🔹 **Navigiere über die Seitenleiste zur Unterseite „Notenrechner“**, um deine Noten einzugeben.
    """)

    st.markdown("### 📌 Anleitung:")
    st.write("""
    1️⃣ Klicke links in der **Seitenleiste** auf **"Notenrechner"**  
    2️⃣ Gib deine Noten für jedes Modul ein  
    3️⃣ Drücke auf **"Berechnen"**, um deinen Notendurchschnitt zu sehen  
    4️⃣ Schaue dir das Balkendiagramm mit deiner Notenverteilung an  
    """)

    st.markdown("---")
    st.write("👨‍🎓 Entwickelt für das **2. Semester (30 ECTS)**")

    st.write("""
    Diese App wurde von folgenden Personen entwickelt:
    - Wanda Schneid (schnewan@students.zhaw.ch)
    - Riccardo Reich (reichri1@students.zhaw.ch)

    Diese App ist das leere Gerüst für die App-Entwicklung im Modul Informatik 2 (BMLD/ZHAW)
    """)
