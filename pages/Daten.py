import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Überprüfen, ob die Seite im richtigen Kontext aufgerufen wird
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py') 

st.title("📊 Gespeicherte Noten")

# Überprüfen, ob Notendaten vorhanden sind
if 'data_df' not in st.session_state or st.session_state['data_df'].empty:
    st.warning("⚠️ Noch keine Noten gespeichert. Bitte zuerst Noten eingeben und berechnen.")
else:
    # Noten aus Session State laden
    df = st.session_state['data_df']

    # Falls Module oder Noten als Listen gespeichert wurden, aufsplitten
    expanded_rows = []
    for _, row in df.iterrows():
        try:
            # Prüfen, ob die Werte als Listen gespeichert wurden, und dann aufsplitten
            modules = eval(row['module']) if isinstance(row['module'], str) and row['module'].startswith("[") else [row['module']]
            grades = eval(row['grades']) if isinstance(row['grades'], str) and row['grades'].startswith("[") else [row['grades']]
            
            # Nur Zeilen mit gleicher Länge von Modulen und Noten übernehmen
            if len(modules) == len(grades):
                for mod, grade in zip(modules, grades):
                    expanded_rows.append({'Module': mod, 'Noten': grade, 'Datum': row['timestamp']})
            else:
                st.warning(f"⚠️ Inkonsistente Zeile übersprungen: {row}")

        except Exception as e:
            st.warning(f"⚠️ Fehlerhafte Zeile entfernt: {row}")

    # Erstellen eines neuen DataFrames mit den gesplitteten Zeilen
    df = pd.DataFrame(expanded_rows)

    # Nur gültige Einträge behalten
    df = df.dropna(subset=['Module', 'Noten'])

    # Datum formatieren für bessere Lesbarkeit
    df['Datum'] = pd.to_datetime(df['Datum']).dt.strftime('%d.%m.%Y %H:%M:%S')

    # Entferne die letzte Zeile, falls sie eine fehlerhafte oder doppelte Gesamtzeile ist
    if not df.empty:
        df = df.iloc[:-1]

    # Farbige Hervorhebung basierend auf Datum/Uhrzeit
    def highlight_groups(s):
        colors = ["#FFDDC1", "#FFABAB", "#FFC3A0", "#D5AAFF", "#85E3FF", "#B9FBC0"]
        unique_timestamps = df["Datum"].unique()
        color_map = {timestamp: colors[i % len(colors)] for i, timestamp in enumerate(unique_timestamps)}
        return [f'background-color: {color_map[val]}' if val in color_map else '' for val in s]

    # Tabelle mit farblicher Unterscheidung anzeigen
    st.subheader("📋 Deine gespeicherten Noten")
    st.dataframe(df.style.apply(highlight_groups, subset=['Datum']))

# Option, um Noten zu löschen
if st.button("📤 Noten zurücksetzen"):
    st.session_state['data_df'] = pd.DataFrame(columns=['Module', 'Noten', 'Datum'])
    st.success("✅ Noten erfolgreich zurückgesetzt!")