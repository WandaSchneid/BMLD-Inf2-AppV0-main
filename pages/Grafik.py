import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Login-Überprüfung
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py')

st.title("📊 Grafik")
st.write("Hier kannst du deine gespeicherten Notendaten und deren Entwicklung über die Zeit einsehen.")

# Laden der gespeicherten Daten
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    df = st.session_state['data_df'].copy()
    
    # Sicherstellen, dass 'timestamp' ein Datetime-Typ ist
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Sicherstellen, dass 'average' numerisch ist
    df['average'] = pd.to_numeric(df['average'], errors='coerce')
    
    # Entfernen von Zeilen mit ungültigen Werten
    df = df.dropna(subset=['timestamp', 'average'])
    
    # Sortieren nach Datum (von früh nach spät)
    df = df.sort_values(by='timestamp')

    # Mittelwerte für gleiche Zeitstempel berechnen
    df_avg = df.groupby('timestamp', as_index=True)['average'].mean()

    # Sicherstellen, dass die Daten nach Zeit aufsteigend sortiert sind
    df_avg = df_avg.sort_index()

    # Fortlaufende Indexwerte für die X-Achse generieren (statt Zeitstempel)
    x_values = range(len(df_avg))  # 0, 1, 2, 3, ...

    st.subheader("📊 Durchschnittsverlauf")
    fig, ax = plt.subplots(figsize=(8, 5))

    # Linien-Plot mit Datenpunkten
    ax.plot(x_values, df_avg.values, marker='o', linestyle='-', color='blue', label='Durchschnitt')

    ax.set_ylabel("Durchschnitt")
    ax.set_xlabel("Datum")  # Änderung: Messpunkt -> Datum
    ax.set_title("Entwicklung des Durchschnitts")
    ax.legend()

    # Setzt die X-Achsen-Ticks auf die tatsächlichen Datenpunkte (keine Zeitstempel)
    ax.set_xticks(x_values)
    ax.set_xticklabels(df_avg.index.strftime('%Y-%m-%d'), rotation=45)

    st.pyplot(fig)
else:
    st.warning("Keine gespeicherten Daten vorhanden.")