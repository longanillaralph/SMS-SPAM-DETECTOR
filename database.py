import os
from dotenv import load_dotenv

try:
    import streamlit as st

    HOST = st.secrets["DB_HOST"]
    PORT = st.secrets["DB_PORT"]
    DATABASE = st.secrets["DB_NAME"]
    USERNAME = st.secrets["DB_USER"]
    PASSWORD = st.secrets["DB_PASSWORD"]

except Exception:
    load_dotenv()

    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DATABASE = os.getenv("DB_NAME")
    USERNAME = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")