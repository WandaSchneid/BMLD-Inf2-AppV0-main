import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Überprüfen, ob die Seite im richtigen Kontext aufgerufen wird
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py') 

st.title("📋 Notenübersicht BMLD Frühlingssemester 2025")

# Daten abrufen
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    df = st.session_state['data_df'].copy()

    # Entferne die ersten beiden Zeilen, die Listen enthalten
    df = df.iloc[2:].reset_index(drop=True)

    # Spalten umbenennen
    df = df.rename(columns={'module': 'Modul', 'grades': 'Noten', 'timestamp': 'Zeitpunkt'})

    # Falls 'Modul' Listen enthält, konvertiere sie in Strings
    df['Modul'] = df['Modul'].apply(lambda x: x[0] if isinstance(x, list) else x)

    # Gruppiere die Daten nach Modul
    module_gruppen = df.groupby("Modul")

    for modulname, moduldaten in module_gruppen:
        # Zeige die Tabelle für jedes Modul
        st.subheader(f"📑 Notenübersicht für {modulname}")
        st.dataframe(moduldaten)

        # Abstand zwischen den Tabellen
        st.markdown("---")
else:
    st.warning("❌ Noch keine Noten gespeichert!")
