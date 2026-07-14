import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report,roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import joblib

def preprocess_data(dataset):
    data = pd.read_csv(dataset, encoding= "latin1")
    data = data.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'])

    data = data.rename(columns={
        "v1":"label",
        "v2":"message"})
    data["label"] = data["label"].map({
        "ham": 0,
        "spam": 1
    })
      
    X = data['message']
    y = data['label']

    return data, X, y

def build_pipeline():
    pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer(
        stop_words= "english",
        lowercase= True,
        max_features= 5000,
        ngram_range=(1,20),
        min_df= 2,
        max_df= 0.95,
        analyzer="char_wb"
    )),
    ("model", LogisticRegression(
        max_iter=1000,
        C=0.5,
        class_weight="balanced"
    ))])
    
    return pipeline

def split_test_train_data(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y, 
                                                        test_size= 0.2, 
                                                        random_state= 42,
                                                        stratify= y)
    X_test_text = X_test.copy()

    return X_train, X_test, y_train, y_test, X_test_text

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    return predictions, probabilities, metrics

def show_false_negatives(X_test, y_test, predictions):
    results = pd.DataFrame({
    "message": X_test_text,
    "actual": y_test,
    "predicted": predictions
})

    false_negatives = results[
    (results["actual"] == 1) &
    (results["predicted"] == 0)
]
    
    print(false_negatives)
if __name__ == "__main__":

    data, X, y = preprocess_data("Data\\spam.csv")

    X_train, X_test, y_train, y_test, X_test_text = split_test_train_data(X, y)

    model = build_pipeline()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    predictions, probabilities, metrics = evaluate_model(model, X_test, y_test)
    print(metrics)
        
    show_false_negatives(X_test, y_test, predictions)

    joblib.dump(model, "model\\spam_classifier.pkl")