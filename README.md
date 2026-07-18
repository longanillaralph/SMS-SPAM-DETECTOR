# SMS Spam Detector

A machine learning-powered SMS spam detection system built with scikit-learn and logistic regression. This project classifies SMS messages as spam or legitimate using a trained ML model with database integration for persistence and model management.

**Live Demo:** https://sms-spam-detector-by-neyaa.streamlit.app/

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Database Setup](#database-setup)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project implements an end-to-end spam detection pipeline:

1. **Data Processing** – Clean and prepare SMS datasets for training
2. **Model Training** – Train a logistic regression classifier with scikit-learn
3. **Model Persistence** – Export and reload trained models
4. **Database Integration** – Store messages, predictions, and model metadata in MySQL (Railway)
5. **Web Interface** – Streamlit app for real-time predictions and model monitoring
6. **Deployment** – Production-ready containerized setup

The system demonstrates practical ML engineering skills including data pipeline design, model serialization, cloud database management, and model serving.

---

## Project Structure

```
sms-spam-detector/
├── .streamlit/              # Streamlit configuration
├── devcontainer/            # Development container setup
├── Data/                    # Dataset folder (raw SMS data)
├── Model/                   # Trained model artifacts
├── Notebooks/               # Jupyter notebooks for exploration and analysis
├── src/                     # Source code modules
├── __pycache__/            # Python cache
├── app.py                  # Streamlit main application
├── create_table.py         # Database schema initialization
├── database.py             # Database connection and utilities
├── models.py               # Model definitions and training logic
├── requirements.txt        # Python dependencies
├── test_connection.py      # Database connectivity tests
└── README.md               # This file
```

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit web interface for predictions and monitoring |
| `models.py` | Model training, evaluation, and inference logic |
| `database.py` | MySQL connection handling and CRUD operations |
| `create_table.py` | Initialize database schema and tables |
| `test_connection.py` | Verify database connectivity (debugging) |
| `requirements.txt` | Project dependencies and versions |

---

## Features

✅ **Logistic Regression Classifier** – Fast, interpretable spam detection  
✅ **Real-time Predictions** – Classify SMS messages instantly  
✅ **Model Persistence** – Save and load trained models for reproducibility  
✅ **Database Storage** – MySQL backend for messages, predictions, and metrics  
✅ **Streamlit Dashboard** – Interactive web interface for users and analysts  
✅ **Dev Container** – Consistent development environment setup  
✅ **Cloud Deployment** – Railway MySQL integration for scalability  
✅ **Model Versioning** – Track multiple model versions and performance  

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.x |
| **ML Framework** | scikit-learn |
| **Database** | MySQL (hosted on Railway) |
| **Web Framework** | Streamlit |
| **Containerization** | Docker (dev container) |
| **Data Processing** | pandas, NumPy |
| **Notebooks** | Jupyter |

---

## Installation

### Prerequisites

- Python 3.8+
- pip or poetry
- MySQL database (local or Railway)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/longanillaraph/SMS-SPAM-DETECTOR.git
   cd sms-spam-detector
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with your Railway MySQL credentials:
   ```
   DB_HOST=your_railway_host
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=spam_detector
   DB_PORT=3306
   ```

5. **Initialize the database**
   ```bash
   python create_table.py
   ```

6. **Test database connection**
   ```bash
   python test_connection.py
   ```

### Dev Container Setup

If using VS Code with the Remote Containers extension:

1. Open the project in VS Code
2. Click "Reopen in Container" when prompted
3. The environment will be automatically configured with all dependencies

---

## Usage

### Running the Streamlit App

Start the web interface for predictions:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. You can:
- Enter an SMS message to check if it's spam
- View prediction confidence scores
- Monitor model performance metrics
- Browse prediction history from the database

### Training the Model

To retrain the model with new data:

```bash
python models.py  # Run the full training pipeline
```

Or import and use in Python:

```python
from models import train_model, evaluate_model
from database import load_spam_data

# Load data
X_train, y_train = load_spam_data()

# Train
model = train_model(X_train, y_train)

# Evaluate
metrics = evaluate_model(model, X_test, y_test)
print(metrics)
```

### Making Predictions

```python
from models import predict_spam
import joblib

# Load the trained model
model = joblib.load('Model/spam_model.pkl')

# Predict
message = "Win $1000! Click here now!"
is_spam, confidence = predict_spam(model, message)
print(f"Spam: {is_spam}, Confidence: {confidence:.2f}")
```

### Database Operations

```python
from database import insert_prediction, get_recent_predictions

# Store a prediction
insert_prediction(message="Test", is_spam=True, confidence=0.95)

# Retrieve recent predictions
predictions = get_recent_predictions(limit=10)
for pred in predictions:
    print(pred)
```

---

## Model Details

### Algorithm

**Logistic Regression** with scikit-learn's `LogisticRegression`:
- **Solver:** lbfgs
- **Max Iterations:** 1000
- **Features:** TF-IDF vectorized text from SMS messages
- **Training Size:** ~5,500 SMS messages (ham + spam)

### Performance Metrics

The model evaluation includes:
- **Accuracy** – Overall correctness rate
- **Precision** – True positive rate among predicted spam
- **Recall** – True positive rate among actual spam
- **F1 Score** – Harmonic mean of precision and recall
- **Confusion Matrix** – TP, FP, TN, FN breakdown

### Model Artifacts

- `Model/spam_model.pkl` – Trained logistic regression classifier
- `Model/tfidf_vectorizer.pkl` – TF-IDF transformer for text featurization

### Retraining Pipeline

To retrain with new data:

1. Prepare labeled SMS dataset (message, label)
2. Load and preprocess data
3. Vectorize text using TF-IDF
4. Train logistic regression
5. Evaluate on test set
6. Save model and vectorizer
7. Deploy new model version

---

## Database Setup

### Schema

The project uses MySQL with the following tables:

**`messages` table:**
```sql
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    is_spam BOOLEAN NOT NULL,
    confidence FLOAT NOT NULL,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Railway MySQL Setup

1. Create a Railway project: https://railway.app
2. Add MySQL plugin
3. Get connection details from Railway dashboard
4. Set environment variables in `.env`
5. Run `python create_table.py` to initialize schema

### Connection Testing

```bash
python test_connection.py
```

This will verify MySQL connectivity and display database info.

---

## Deployment

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Set environment variables in Streamlit Secrets
5. Deploy!

**Current deployment:** https://sms-spam-detector-by-neyaa.streamlit.app/

### Docker Deployment

Build a container:

```bash
docker build -t sms-spam-detector .
docker run -p 8501:8501 --env-file .env sms-spam-detector
```

### Railway Deployment

1. Connect GitHub repo to Railway
2. Add MySQL plugin
3. Set environment variables
4. Deploy the Streamlit app service

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and test thoroughly
4. Commit with clear messages (`git commit -m "Add feature: ..."`)
5. Push to your branch (`git push origin feature/your-feature`)
6. Open a Pull Request

### Development Guidelines

- Use Python 3.8+ type hints where applicable
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Test database operations thoroughly before merging
- Update `requirements.txt` if adding dependencies

---

## Troubleshooting

### Database Connection Issues

**Problem:** `OperationalError: (2003, "Can't connect to MySQL server")`

**Solution:**
- Verify Railway MySQL credentials in `.env`
- Check that Railway MySQL is running
- Ensure whitelist IP in Railway settings
- Run `python test_connection.py` for detailed error messages

### Model Not Found

**Problem:** `FileNotFoundError: [Errno 2] No such file or directory: 'Model/spam_model.pkl'`

**Solution:**
- Run `python models.py` to train and save the model
- Check that the `Model/` directory exists

### Streamlit Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

---

## Project Status

- ✅ Core ML model (logistic regression)
- ✅ Database integration (MySQL + Railway)
- ✅ Streamlit web interface
- ✅ Model persistence and versioning
- 🔄 Advanced feature engineering (in progress)
- 📋 Model interpretability dashboard (planned)
- 📋 Batch prediction API (planned)

---

## License

This project is open source and available under the MIT License.

---

## Author

**Eyan** | [GitHub](https://github.com/longanillaraph)

---

## Acknowledgments

- Dataset: UCI SMS Spam Collection
- Framework: scikit-learn, Streamlit
- Hosting: Railway, Streamlit Cloud
- Inspired by practical ML engineering best practices

---

## Questions or Issues?

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Open a new issue with detailed information

Happy spam detecting! 🚀
