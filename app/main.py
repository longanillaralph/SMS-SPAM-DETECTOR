from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from app.schema import SMSRequest
from app.predict import predict_sms
from sqlmodel import Session, select
from app.database import engine, init_db
from app.models import Prediction

app = FastAPI()

# allow local dev frontends (Live Server) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/predict")
def predict(data: SMSRequest):
    # run prediction first
    try:
        prediction, probability = predict_sms(data.message)
    except Exception as exc:
        return JSONResponse(status_code=500, content={"detail": f"Prediction error: {exc}"})

    new_prediction = Prediction(
        message=data.message,
        prediction="Spam" if prediction else "Ham",
        probability=float(probability),
    )

    # attempt to save prediction to DB but do not fail the endpoint if DB is unavailable
    db_saved = True
    db_error = None
    try:
        with Session(engine) as session:
            session.add(new_prediction)
            session.commit()
    except Exception as exc:
        db_saved = False
        db_error = str(exc)

    response_content = {
        "prediction": "Spam" if prediction else "Ham",
        "probability": float(probability),
        "db_saved": db_saved,
    }
    if db_error:
        response_content["db_error"] = db_error

    return JSONResponse(status_code=200, content=response_content)


@app.get("/history")
def history():
    try:
        with Session(engine) as session:
            history = session.exec(select(Prediction)).all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc

    return history