from datetime import datetime
from sqlmodel import SQLModel, Field


class Prediction(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    message: str
    prediction: str
    probability: float
    created_at: datetime = Field(default_factory=datetime.now)