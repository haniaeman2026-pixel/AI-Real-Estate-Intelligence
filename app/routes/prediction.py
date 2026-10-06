from fastapi import APIRouter, HTTPException

from app.schemas.property_schema import PredictionRequest
from app.services.prediction_service import (
    predict_price,
    model_status,
)


router = APIRouter()


@router.get("/status")
def status():
    """
    Check the status of the price prediction model.
    """

    return model_status()


@router.post("/predict")
def predict(payload: PredictionRequest):
    """
    Predict property sale price using the trained ML model.
    """

    try:
        return predict_price(payload.model_dump())

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )