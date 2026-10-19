from database import Base, engine
from models import Prediction

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")