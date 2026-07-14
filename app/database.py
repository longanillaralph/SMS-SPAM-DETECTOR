from dotenv import load_dotenv
import os
from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".venv" / ".env")

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)