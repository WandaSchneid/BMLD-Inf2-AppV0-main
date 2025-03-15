import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Überprüfen, ob die Seite im richtigen Kontext aufgerufen wird
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py') 

st.title("📊 Durchschnittsnote BMLD Frühlingssemester 2025")

# Daten abrufen
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    df = st.session_state['data_df'].copy()
    
    # Entferne die ersten beiden Zeilen
    df = df.iloc[2:].reset_index(drop=True)
    
    # Spalten umbenennen
    df = df.rename(columns={'module': 'Moldule', 'grades': 'Noten', 'timestamp': 'Datum'})
    
    # Falls die 'Datum'-Spalte Listen enthält, extrahiere nur das erste Element
    df['Datum'] = df['Datum'].apply(lambda x: x[0] if isinstance(x, list) else x)
    
    # Stelle sicher, dass 'Datum' ein echtes Datumsformat hat
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.date  # Nur das Datum extrahieren
    
    # Stelle sicher, dass die 'Noten'-Spalte numerisch ist
    df['Noten'] = pd.to_numeric(df['Noten'], errors='coerce')
    df = df.dropna(subset=['Noten'])
    
    # Gruppiere die Daten nach Datum und berechne den Durchschnitt
    durchschnittswerte = df.groupby('Datum')['Noten'].mean()
    
    # Setze das Startdatum auf das erste Eingabedatum
    startdatum = df['Datum'].min()
    
    st.subheader("📈 Entwicklung deines Durchschnitts")
    
    fig, ax = plt.subplots()
    ax.plot(durchschnittswerte.index, durchschnittswerte.values, marker='o', linestyle='-', color='b')
    ax.set_xlabel("Datum")
    ax.set_ylabel("Durchschnittsnote")
    ax.set_title("Verlauf der Durchschnittsnote")
    ax.set_xlim(left=startdatum)  # Setze das Startdatum der x-Achse
    plt.xticks(rotation=45, ha='right')
    
    st.pyplot(fig)
else:
    st.warning("❌ Noch keine Durchschnittswerte gespeichert!")