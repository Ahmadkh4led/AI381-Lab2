
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_fee",
    "contract",
    "internet_service",
    "support_calls",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    if not MODEL_PATH.is_file():
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)
    yield


app = FastAPI(
    title="AI381 Lab 2 Churn API",
    lifespan=lifespan,
)

class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: str = Field(min_length=1)
    internet_service: str = Field(min_length=1)
    support_calls: int = Field(ge=0)





@app.get("/health")
def health():
    if "model" not in globals():
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: Customer):
    if "model" not in globals():
        raise HTTPException(status_code=503, detail="Model not loaded")

    X = pd.DataFrame([customer.model_dump()])[FEATURES]
    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}
