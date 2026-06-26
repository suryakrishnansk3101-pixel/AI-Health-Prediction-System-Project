from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parent / "health_model.pkl"
RISK_LABELS = {
    0: "Healthy - Blood test values are within normal range.",
    1: "Prediabetes Risk - Elevated glucose level detected. Lifestyle monitoring is recommended.",
    2: "Diabetes Risk - High glucose values detected. Further medical evaluation is recommended.",
    3: "Heart Disease Risk - Elevated cholesterol levels detected. Clinical consultation is advised.",
}


def _load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "ML model not found. Run `python ml/train_model.py` from the backend directory."
        )
    return joblib.load(MODEL_PATH)


def predict_health_risk(glucose, haemoglobin, cholesterol):
    model = _load_model()
    prediction = model.predict([[float(glucose), float(haemoglobin), float(cholesterol)]])[0]
    return RISK_LABELS.get(int(prediction), "Unknown Risk")
