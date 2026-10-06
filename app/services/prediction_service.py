from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

TRAIN_FILE = DATA_DIR / "train.csv"
MODEL_FILE = MODEL_DIR / "price_model.joblib"


# ============================================================
# MODEL FEATURES
# ============================================================

NUMERIC_FEATURES = [
    "OverallQual",
    "GrLivArea",
    "YearBuilt",
    "TotalBsmtSF",
    "GarageCars",
    "FullBath",
    "BedroomAbvGr",
    "LotArea",
]

CATEGORICAL_FEATURES = [
    "Neighborhood",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TARGET = "SalePrice"


# ============================================================
# GLOBAL MODEL
# ============================================================

model = None


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    global model

    if not TRAIN_FILE.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {TRAIN_FILE}"
        )

    print("Loading real estate dataset...")

    df = pd.read_csv(TRAIN_FILE)

    print(f"Dataset loaded: {df.shape}")

    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    required_columns = FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Select features and target
    # --------------------------------------------------------

    X = df[FEATURES].copy()

    y = df[TARGET].copy()

    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    # --------------------------------------------------------
    # Random Forest Model
    # --------------------------------------------------------

    random_forest = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )

    # --------------------------------------------------------
    # Complete ML Pipeline
    # --------------------------------------------------------

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                random_forest,
            ),
        ]
    )

    print("Training Random Forest model...")

    pipeline.fit(X, y)

    print("Model training completed.")

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        MODEL_FILE,
    )

    print(
        f"Model saved successfully: {MODEL_FILE}"
    )

    model = pipeline

    return model


# ============================================================
# LOAD OR TRAIN MODEL
# ============================================================

def initialize_model():

    global model

    if MODEL_FILE.exists():

        print("Loading saved ML model...")

        model = joblib.load(
            MODEL_FILE
        )

        print("Saved ML model loaded.")

    else:

        print(
            "Saved model not found. "
            "Training a new model..."
        )

        train_model()


# ============================================================
# MODEL STATUS
# ============================================================

def model_status():

    return {
        "feature": "ML Price Prediction",
        "model": "Random Forest Regressor",
        "status": "online" if model is not None else "offline",
        "model_file": str(MODEL_FILE),
    }


# ============================================================
# PRICE PREDICTION
# ============================================================

def predict_price(property_data: dict):

    global model

    if model is None:
        initialize_model()

    # Convert API fields to dataset column names
    input_data = pd.DataFrame(
        [
            {
                "OverallQual": property_data["overall_qual"],
                "GrLivArea": property_data["gr_liv_area"],
                "YearBuilt": property_data["year_built"],
                "TotalBsmtSF": property_data["total_bsmt_sf"],
                "GarageCars": property_data["garage_cars"],
                "FullBath": property_data["full_bath"],
                "BedroomAbvGr": property_data["bedroom_abv_gr"],
                "LotArea": property_data["lot_area"],
                "Neighborhood": property_data["neighborhood"],
            }
        ]
    )

    prediction = model.predict(
        input_data
    )[0]

    predicted_price = round(
        float(prediction),
        2,
    )

    return {
        "success": True,
        "predicted_price": predicted_price,
        "currency": "USD",
        "model": "Random Forest Regressor",
        "message": (
            "Estimated property price generated "
            "from the trained Ames Housing dataset."
        ),
    }