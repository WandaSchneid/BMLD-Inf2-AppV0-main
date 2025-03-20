import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd  # Import pandas
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Überprüfen, ob die Seite im richtigen Kontext aufgerufen wird
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py') 

st.title("Notenrechner BMLD Frühlingssemester 2025")

st.write("Diese Seite berechnet deine Note.")

page = "Notenrechner:"
if page == "Notenrechner:":
    st.title("🎓 Notenrechner")

    st.write("🔢 **Gib deine Noten ein, um deinen gewichteten Durchschnitt zu berechnen.**")

    # Liste der Module mit ECTS-Punkten
    module = {
        "Biologie 2": 3, "Chemie 2": 3, "Informatik 2": 2, "Mathematik 2": 3,
        "Physik": 3, "Englisch 2": 2, "Gesellschaftlicher Kontext und Sprache 2": 2,
        "Klinische Chemie und Immunologie 1": 2, "Histologie und Zytologie 1": 3,
        "Medizinische Mikrobiologie 2": 2, "Haematologie und Haemostaseologie 2": 3,
        "Grundlagenpraktikum 2": 3
    }

    noten = {}
    with st.form("noten_form"):
        st.subheader("📌 Noteneingabe:")

        for modul, ects in module.items():
            noten[modul] = st.number_input(f"{modul} (ECTS: {ects})", 
                                           min_value=1.0, max_value=6.0, value=3.0, step=0.1)

        submit_button = st.form_submit_button("Berechnen")

    if submit_button:
        sum_ects = sum(module.values())
        sum_weighted = sum(noten[modul] * module[modul] for modul in module)

        if sum_ects > 0:
            durchschnitt = sum_weighted / sum_ects
            st.success(f"🎯 Dein gewichteter Notendurchschnitt: **{durchschnitt:.2f}**")
        else:
            st.error("⚠️ Fehler: Keine gültigen ECTS-Punkte eingegeben.")

        # Notenverteilung als Balkendiagramm
        st.subheader("📊 Notenverteilung")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(noten.keys(), noten.values(), color='skyblue')
        ax.set_ylabel("Note")
        ax.set_xlabel("Module")
        ax.set_ylim(1, 6)
        ax.set_title("Deine Notenübersicht")
        plt.xticks(rotation=45, ha='right')
        
        st.pyplot(fig)

        # Definiere das result Dictionary
        result = {
            "module": list(noten.keys()),
            "grades": list(noten.values()),
            "average": [durchschnitt] * len(noten),  # Wiederhole den Durchschnitt für jedes Modul
            "timestamp": [pd.Timestamp.now()] * len(noten)  # Füge einen Zeitstempel für jedes Modul hinzu
        }

        # Speichern Sie die Daten in der Session
        if 'data_df' not in st.session_state:
            st.session_state['data_df'] = pd.DataFrame(columns=['module', 'grades', 'average', 'timestamp'])

        # Erstellen Sie einen DataFrame aus dem result-Dictionary
        new_data = pd.DataFrame(result)

        # Fügen Sie die neuen Daten zum bestehenden DataFrame hinzu
        st.session_state['data_df'] = pd.concat([st.session_state['data_df'], new_data], ignore_index=True)

        # Speichern Sie die Daten persistent
        data_manager = DataManager()
        for _, row in new_data.iterrows():
            data_manager.append_record(session_state_key='data_df', record_dict=row.to_dict())