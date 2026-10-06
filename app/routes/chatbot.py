from fastapi import APIRouter, HTTPException

from app.schemas.property_schema import ChatRequest
from app.services.ai_service import chat


router = APIRouter()


@router.get("/status")
def status():
    """
    Check AI assistant status.
    """

    return {
        "feature": "AI Real Estate Assistant",
        "status": "online",
    }


@router.post("/chat")
def assistant(
    payload: ChatRequest,
):
    """
    Send a question to the AI real estate assistant.
    """

    try:
        return chat(payload.message)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )