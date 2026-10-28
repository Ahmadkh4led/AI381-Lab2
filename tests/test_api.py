
from fastapi.testclient import TestClient

import src.app.main as api
from src.app.main import app

VALID_CUSTOMER = {
    "tenure_months": 72,
    "monthly_fee": 45.0,
    "contract": "two-year",
    "internet_service": "dsl",
    "support_calls": 1,
}


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_loads():
    with TestClient(app):
        assert api.model is not None
        assert hasattr(api.model, "predict_proba")


def test_predict_returns_probability():
    with TestClient(app) as client:
        response = client.post("/predict", json=VALID_CUSTOMER)

    assert response.status_code == 200
    result = response.json()
    assert "churn_probability" in result
    assert 0 <= result["churn_probability"] <= 1


def test_invalid_input_is_rejected():
    customer = VALID_CUSTOMER.copy()
    del customer["contract"]

    with TestClient(app) as client:
        response = client.post("/predict", json=customer)

    assert response.status_code == 422


def test_negative_tenure_is_rejected():
    customer = VALID_CUSTOMER.copy()
    customer["tenure_months"] = -1

    with TestClient(app) as client:
        response = client.post("/predict", json=customer)

    assert response.status_code == 422


def test_prediction_is_deterministic():
    with TestClient(app) as client:
        first = client.post("/predict", json=VALID_CUSTOMER)
        second = client.post("/predict", json=VALID_CUSTOMER)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
