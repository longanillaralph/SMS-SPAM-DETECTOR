# SMS Spam Detector

A machine learning-powered web application that classifies SMS messages
as **spam** or **ham (legitimate)**. The application uses a trained
machine learning model, a Streamlit interface, and PostgreSQL to store
prediction records.

**Live Demo:** https://sms-spam-detector-by-neyaa.streamlit.app/

## Features

-   **SMS classification:** Predict whether a message is spam or
    legitimate.
-   **Streamlit interface:** Enter an optional name and an SMS message
    through a web interface.
-   **Prediction persistence:** Save prediction records to a PostgreSQL
    database.
-   **SQLAlchemy integration:** Manage database connections and the
    `predictions` table through SQLAlchemy.
-   **Environment configuration:** Keep local database credentials in a
    `.env` file rather than hard-coding them in source code.
-   **Virtual environment support:** Isolate Python dependencies for
    local development.

## Tech Stack

  -----------------------------------------------------------------------
  Component                           Technology
  ----------------------------------- -----------------------------------
  Language                            Python

  Machine learning                    scikit-learn

  Web interface                       Streamlit

  Database                            PostgreSQL

  Database toolkit / ORM              SQLAlchemy

  PostgreSQL driver                   Psycopg

  Environment variables               python-dotenv

  Model persistence                   Pickle/joblib artifacts, depending
                                      on the project files
  -----------------------------------------------------------------------

## Project Structure

The main files and folders include:

``` text
SMS-SPAM-DETECTOR/
├── .streamlit/          # Streamlit configuration
├── Data/                # Dataset files
├── Model/               # Saved model artifacts
├── Notebooks/           # Jupyter notebooks
├── src/                 # Supporting source code
├── app.py               # Streamlit application
├── database.py          # PostgreSQL connection and SQLAlchemy setup
├── models.py            # SQLAlchemy Prediction model definitions
├── requirements.txt     # Python dependencies
├── test_connection.py   # Database connection test
├── .env                 # Local environment variables (create locally; do not commit)
├── .gitignore           # Files Git should ignore
└── README.md
```

Your local project may contain additional files. Keep the `venv/`
virtual environment out of version control.

## Requirements

-   Python installed on your computer
-   PostgreSQL installed and running, or access to a PostgreSQL server
-   Git (optional, for cloning the repository)

## Installation and Local Setup

### 1. Clone the repository

``` bash
git clone https://github.com/longanillaraph/SMS-SPAM-DETECTOR.git
cd SMS-SPAM-DETECTOR
```

If you already have the project on your computer, open its folder in VS
Code and skip this step.

### 2. Create and activate a virtual environment

On Windows PowerShell:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

``` bat
venv\Scripts\activate
```

On macOS or Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

When activation succeeds, the terminal normally shows `(venv)`.

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

The project uses PostgreSQL through Psycopg. If these packages are not
already in `requirements.txt`, install them in the active virtual
environment:

``` bash
python -m pip install "psycopg[binary]" python-dotenv sqlalchemy
```

### 4. Create the PostgreSQL database

In pgAdmin 4:

1.  Connect to your PostgreSQL server.
2.  Right-click **Databases** and choose **Create → Database**.
3.  Use a database name such as `sms_spam_detector`.
4.  Save the database.

Use the actual database name you created in the configuration below.
PostgreSQL database names can be case-sensitive when created with quoted
uppercase letters.

### 5. Configure environment variables

Create a `.env` file in the project root, alongside `app.py` and
`database.py`:

``` dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sms_spam_detector
DB_USER=postgres
DB_PASSWORD=replace_with_your_postgresql_password
```

Replace the example database name, username, and password with the
values for your PostgreSQL setup. The port `5432` is PostgreSQL's
default; use your server's configured port if different.

**Security:** Do not commit `.env` or real database credentials to
GitHub. Add the following to the root `.gitignore`:

``` gitignore
.env
venv/
__pycache__/
```

### 6. Test the database connection

Run:

``` bash
python test_connection.py
```

A successful test should report that the PostgreSQL connection
succeeded. If it fails, verify that PostgreSQL is running, the database
exists, and the `.env` values are correct.

### 7. Create the prediction table

The SQLAlchemy `Prediction` model defines a `predictions` table with
fields for an ID, optional name, message, prediction, probability, and
creation timestamp.

If the project does not already have a database initialization script,
create `init_db.py` in the project root:

``` python
from database import Base, engine
from models import Prediction

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
```

Run it once:

``` bash
python init_db.py
```

This creates tables defined on the imported `Base` if they do not
already exist. Make sure `models.py` imports the same `Base` object from
`database.py`; separate declarative bases will not share metadata. This
command does not migrate or copy data from a previous MySQL database.

## Run the Application

With the virtual environment activated and dependencies installed, run:

``` bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

``` text
http://localhost:8501
```

Enter an optional name, type or paste an SMS message, and click
**Analyze Message** to view the prediction.

## Database Model

The `Prediction` SQLAlchemy model represents the `predictions` table:

  -----------------------------------------------------------------------
  Column                              Purpose
  ----------------------------------- -----------------------------------
  `id`                                Integer primary key

  `name`                              Optional name associated with the
                                      prediction

  `message`                           SMS message submitted for
                                      classification

  `prediction`                        Predicted class, such as spam or
                                      ham

  `probability`                       Model probability/confidence value
                                      stored by the application

  `created_at`                        Timestamp assigned when the record
                                      is created
  -----------------------------------------------------------------------

The application must explicitly save predictions through its database
logic. Creating the table alone does not automatically save records.

## Model Evaluation and Future Improvements

Potential next steps include:

-   Report precision, recall, F1-score, and a confusion matrix using a
    held-out test set.
-   Add a prediction-history view with pagination and filters.
-   Add summary charts for saved predictions.
-   Add automated tests for prediction and database logic.
-   Use database migrations when the schema changes.
-   Configure a hosted PostgreSQL database and deploy the updated
    version.

Only report evaluation metrics after measuring them on the actual
trained model and test data.

## Troubleshooting

### `ModuleNotFoundError: No module named 'psycopg'`

Activate the project's virtual environment and install the driver:

``` bash
python -m pip install "psycopg[binary]"
```

### `database "..." does not exist`

Check `DB_NAME` in `.env` against the exact database name listed under
**Servers → PostgreSQL → Databases** in pgAdmin. Refresh the Databases
node if needed.

### `invalid literal for int() with base 10: 'None'`

The database URL is receiving an invalid port value. Set `DB_PORT` to
the PostgreSQL server's numeric port (commonly `5432`) and verify that
the environment variables are being loaded.

### Password authentication failed

Verify `DB_USER` and `DB_PASSWORD`. Do not share database passwords in
issue reports or public repositories.

### Streamlit port is already in use

Try another port:

``` bash
python -m streamlit run app.py --server.port 8502
```

## Deployment

The project has a published Streamlit demo:

https://sms-spam-detector-by-neyaa.streamlit.app/

For a deployment that uses PostgreSQL, configure the corresponding
database secrets in the hosting platform and ensure the hosted database
is reachable from the app. Do not use local `localhost` database
settings for a cloud deployment unless the database actually runs in the
same environment.

After changing the database backend, verify the deployed app's secrets,
dependencies, and database schema separately. A successful local
connection does not automatically update the hosted application.

## Author

**Eyan** --- [GitHub](https://github.com/longanillaraph)

## Acknowledgments

-   UCI SMS Spam Collection dataset (if used by the training pipeline)
-   scikit-learn
-   Streamlit
-   PostgreSQL
-   SQLAlchemy
