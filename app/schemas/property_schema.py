from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):

    overall_qual: int = Field(
        5,
        ge=1,
        le=10
    )

    gr_liv_area: float = Field(
        1500,
        gt=0
    )

    year_built: int = Field(
        2000,
        ge=1800,
        le=2100
    )

    total_bsmt_sf: float = Field(
        800,
        ge=0
    )

    garage_cars: int = Field(
        2,
        ge=0,
        le=6
    )

    full_bath: int = Field(
        2,
        ge=0,
        le=6
    )

    bedroom_abv_gr: int = Field(
        3,
        ge=0,
        le=10
    )

    lot_area: float = Field(
        8000,
        ge=0
    )

    neighborhood: str = "NAmes"


class RecommendationRequest(BaseModel):

    budget: float = Field(
        ...,
        gt=0
    )

    bedrooms: int = Field(
        3,
        ge=0,
        le=10
    )

    neighborhood: str = ""

    min_area: float = Field(
        0,
        ge=0
    )

    top_k: int = Field(
        6,
        ge=1,
        le=12
    )


class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )


class RAGRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )