from fastapi import APIRouter, HTTPException

from app.schemas.property_schema import RAGRequest
from app.services.rag_service import (
    answer_with_rag,
    rag_status,
)


router = APIRouter()


@router.get("/status")
def status():
    """
    Check RAG knowledge-base status.
    """

    return rag_status()


@router.post("/ask")
def ask(
    payload: RAGRequest,
):
    """
    Ask a question using the RAG knowledge base.
    """

    try:
        return answer_with_rag(payload.question)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )