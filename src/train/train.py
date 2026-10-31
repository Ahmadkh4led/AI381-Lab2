
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "churn_v2.csv"
MODEL_PATH = PROJECT_ROOT / "model.joblib"

NUMERIC_FEATURES = [
    "tenure_months",
    "monthly_fee",
    "support_calls",
]

CATEGORICAL_FEATURES = [
    "contract",
    "internet_service",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "churn"


def main():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    # Load the dataset
    data = pd.read_csv(DATA_PATH)

    # Separate features and target
    X = data[FEATURES]
    y = data[TARGET]

    # Preprocess numerical and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    # Build the machine learning pipeline
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Model accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Save the trained model
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved successfully to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
