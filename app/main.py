from fastapi import FastAPI
from app.schema import SMSRequest
from app.predict import predict_sms
from sqlmodel import Session
from app.database import engine
from app.models import Prediction

app = FastAPI()


@app.get("/")
def home():
    return {"message": "SMS Spam Detector API"}

@app.post("/predict")
def predict(data: SMSRequest):

    prediction, probability = predict_sms(data.message)
    new_prediction = Prediction(
    message=data.message,
    prediction="Spam" if prediction else "Ham",
    probability=float(probability)
)
    with Session(engine) as session:
        session.add(new_prediction)
        session.commit()

    return {
        "prediction": "Spam" if prediction else "Ham",
        "probability": probability
    }