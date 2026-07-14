from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "Model" / "spam_classifier.pkl"
model = joblib.load(MODEL_PATH)


def predict_sms(message: str):
    prediction = model.predict([message])[0]
    probability = model.predict_proba([message])[0][1]

    return prediction, probability