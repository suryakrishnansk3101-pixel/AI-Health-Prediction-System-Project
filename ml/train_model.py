from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


MODEL_PATH = Path(__file__).resolve().parent / "health_model.pkl"
RANDOM_SEED = 42


def build_sample_dataset():
    rng = np.random.default_rng(RANDOM_SEED)
    records = []

    def add_group(count, glucose_range, haemoglobin_range, cholesterol_range, risk):
        for _ in range(count):
            records.append(
                [
                    round(float(rng.uniform(*glucose_range)), 1),
                    round(float(rng.uniform(*haemoglobin_range)), 1),
                    round(float(rng.uniform(*cholesterol_range)), 1),
                    risk,
                ]
            )

    add_group(30, (72, 99), (12.5, 16.5), (125, 189), 0)
    add_group(30, (100, 125), (11.0, 16.0), (150, 219), 1)
    add_group(30, (126, 230), (10.0, 15.8), (160, 239), 2)
    add_group(30, (95, 185), (8.0, 13.2), (240, 360), 3)

    rng.shuffle(records)
    return np.array(records)


def train():
    dataset = build_sample_dataset()
    x = dataset[:, :3]
    y = dataset[:, 3].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=RANDOM_SEED,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train()
