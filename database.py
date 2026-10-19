from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.engine import URL

load_dotenv()

def get_db_config():
    try:
        # Streamlit Cloud secrets
        if "DB_HOST" in st.secrets:
            return {
                "host": st.secrets["DB_HOST"],
                "port": st.secrets["DB_PORT"],
                "database": st.secrets["DB_NAME"],
                "username": st.secrets["DB_USER"],
                "password": st.secrets["DB_PASSWORD"],
            }
    except Exception:
        pass

    # Local .env file
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "sms_spam_detector"),
        "username": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD"),
    }

db = get_db_config()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=db["username"],
    password=db["password"],
    host=db["host"],
    port=int(db["port"]),
    database=db["database"],
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass
