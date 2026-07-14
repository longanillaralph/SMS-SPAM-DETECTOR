from fastapi import FastAPI
from app.schema import SMSRequest
from app.predict import predict_sms

app = FastAPI()


@app.get("/")
def home():
    return {"message": "SMS Spam Detector API"}

@app.post("/predict")
def predict(data: SMSRequest):

    prediction, probability = predict_sms(data.message)

    return {
        "prediction": "Spam" if prediction else "Ham",
        "probability": probability
    }