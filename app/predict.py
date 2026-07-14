import joblib

model = joblib.load("model\\spam_classifier.pkl")


def predict_sms(message: str):
    prediction = model.predict([message])[0]
    probability = model.predict_proba([message])[0][1]

    return prediction, probability