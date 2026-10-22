import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report,roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from pathlib import Path
from datetime import datetime
import shutil

def preprocess_data(dataset):
    """Load one CSV or several CSVs and return one cleaned dataset.

    Each CSV must contain v1 (ham/spam) and v2 (message) columns.
    """
    files = [dataset] if isinstance(dataset, (str, Path)) else list(dataset)
    frames = []

    for file in files:
        data = pd.read_csv(file, encoding="latin1")
        data = data.drop(
            columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],
            errors='ignore'
        )

        data = data.rename(columns={"v1": "label", "v2": "message"})
        required = {"label", "message"}
        if not required.issubset(data.columns):
            raise ValueError(
                f"{file} must contain columns v1 and v2 (or label and message)"
            )
        frames.append(data[["label", "message"]])

    data = pd.concat(frames, ignore_index=True)
    data["label"] = data["label"].astype(str).str.strip().str.lower().map({
        "ham": 0,
        "spam": 1
    })
    data["message"] = data["message"].astype(str).str.strip()
    data = data.dropna(subset=["label", "message"])
    data = data[data["message"] != ""]
    data = data.drop_duplicates(subset=["message"])

    X = data['message']
    y = data['label']

    return data, X, y

def build_pipeline():
    pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer(
        lowercase=True,
        max_features=10000,
        ngram_range=(1, 5),
        min_df=1,
        max_df=0.98,
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
    "message": X_test,
    "actual": y_test,
    "predicted": predictions
})

    false_negatives = results[
    (results["actual"] == 1) &
    (results["predicted"] == 0)
]
    
    print(false_negatives)
if __name__ == "__main__":
    # Every CSV in Data is included on every training run.
    # Add another labeled CSV to Data and run this script again.
    dataset_files = sorted(Path("Data").glob("*.csv"))
    if not dataset_files:
        raise FileNotFoundError("No CSV datasets found in the Data folder.")

    combined_data, X, y = preprocess_data(dataset_files)

    print(f"Datasets: {len(dataset_files)}")
    print(f"Training messages: {len(combined_data)}")
    print("Class counts (0=ham, 1=spam):")
    print(y.value_counts().sort_index().to_string())

    X_train, X_test, y_train, y_test, _ = split_test_train_data(X, y)

    model = build_pipeline()
    model.fit(X_train, y_train)

    predictions, probabilities, metrics = evaluate_model(
        model, X_test, y_test
    )

    print("Evaluation metrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    model_path = Path("Model/spam_classifier.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)

    if model_path.exists():
        backup_path = model_path.with_name(
            f"spam_classifier_{datetime.now():%Y%m%d_%H%M%S}.pkl"
        )
        shutil.copy2(model_path, backup_path)
        print(f"Previous model backed up to {backup_path}")

    joblib.dump(model, model_path)
    print("Updated model saved successfully.")
