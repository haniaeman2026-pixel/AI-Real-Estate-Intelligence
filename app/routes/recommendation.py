from fastapi import APIRouter, HTTPException

from app.schemas.property_schema import RecommendationRequest
from app.services.recommendation_service import recommend


router = APIRouter()


@router.get("/status")
def status():
    """
    Check recommendation engine status.
    """

    return {
        "feature": "Property Recommendation",
        "status": "online",
    }


@router.post("/recommend")
def get_recommendations(
    payload: RecommendationRequest,
):
    """
    Generate property recommendations based
    on user preferences.
    """

    try:
        return recommend(payload.model_dump())

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )