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
import pandas as pd  # Import pandas

st.title('Noten Verlauf')

data_df = st.session_state['data_df']
if data_df.empty:
    st.info('Keine Noten vorhanden. Berechnen Sie Ihre Noten')
    st.stop()

# Sort dataframe by timestamp
data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])
data_df = data_df.sort_values('timestamp', ascending=False)

# Display table
st.dataframe(data_df)