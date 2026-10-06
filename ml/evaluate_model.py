from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "train.csv"
MODEL_FILE = BASE_DIR / "models" / "price_model.joblib"
RESULT_FILE = BASE_DIR / "models" / "model_evaluation.txt"


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "OverallQual",
    "GrLivArea",
    "YearBuilt",
    "TotalBsmtSF",
    "GarageCars",
    "FullBath",
    "BedroomAbvGr",
    "LotArea",
    "Neighborhood",
]

TARGET = "SalePrice"


# ============================================================
# EVALUATION
# ============================================================

def evaluate_model():

    print("=" * 60)
    print("ML MODEL EVALUATION")
    print("=" * 60)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Trained model not found. "
            "Run model training first."
        )

    # Load dataset
    df = pd.read_csv(DATA_FILE)

    X = df[FEATURES]
    y = df[TARGET]

    # Same split used for evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    # Load trained model
    model = joblib.load(MODEL_FILE)

    # Predictions
    predictions = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    # Print results
    print()
    print(f"MAE  : ${mae:,.2f}")
    print(f"RMSE : ${rmse:,.2f}")
    print(f"R²   : {r2:.4f}")
    print()

    # Save results
    RESULT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "AI Real Estate Intelligence Platform\n"
        )

        file.write(
            "Machine Learning Model Evaluation\n"
        )

        file.write(
            "=" * 50 + "\n\n"
        )

        file.write(
            "Model: Random Forest Regressor\n"
        )

        file.write(
            "Dataset: Ames Housing Dataset\n\n"
        )

        file.write(
            f"MAE: ${mae:,.2f}\n"
        )

        file.write(
            f"RMSE: ${rmse:,.2f}\n"
        )

        file.write(
            f"R2 Score: {r2:.4f}\n"
        )

    print(
        f"Evaluation saved to: {RESULT_FILE}"
    )

    print("=" * 60)

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
    }


if __name__ == "__main__":
    evaluate_model()