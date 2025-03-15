import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

# ------------------------------------------------------------
# === Noten Grafik ===
import streamlit as st

st.title('Noten Verlauf')

data_df = st.session_state['data_df']
if data_df.empty:
    st.info('Keine Noten vorhanden. Berechnen Sie Ihre Noten')
    st.stop()

# Noten über Zeit
st.line_chart(data=data_df.set_index('timestamp')['average'], 
                use_container_width=True)
st.caption('Noten Zeitverlauf')

# Notenverteilung als Balkendiagramm
st.bar_chart(data=data_df.set_index('timestamp')['grades'], 
                use_container_width=True)
st.caption('Notenverteilung')

# Module über Zeit
st.line_chart(data=data_df.set_index('timestamp')['module'],
                use_container_width=True)
st.caption('Module über Zeit')