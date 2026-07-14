import joblib

model = joblib.load("model\\spam_classifier.pkl")

while True:
    text = input("Enter message: ")

    prediction = model.predict([text])[0]

    if prediction == 1:
        print("Spam")
    else:
        print("Ham")