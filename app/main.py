from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# ============================================================
# ROUTES
# ============================================================

from app.routes.prediction import router as prediction_router
from app.routes.recommendation import router as recommendation_router
from app.routes.chatbot import router as chatbot_router
from app.routes.rag import router as rag_router


# ============================================================
# SERVICES
# ============================================================

from app.services.prediction_service import initialize_model
from app.services.recommendation_service import (
    initialize_recommendations
)
from app.services.ai_service import initialize_ai
from app.services.rag_service import initialize_rag


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"


# ============================================================
# APPLICATION STARTUP / SHUTDOWN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print()
    print("=" * 65)
    print("       AI REAL ESTATE INTELLIGENCE PLATFORM")
    print("=" * 65)
    print()

    # --------------------------------------------------------
    # 1. MACHINE LEARNING MODEL
    # --------------------------------------------------------

    print("[1/4] Initializing ML price prediction model...")

    try:
        initialize_model()

        print(
            "      ✓ ML price prediction model initialized."
        )

    except Exception as exc:

        print(
            f"      ✗ ML model initialization failed: {exc}"
        )

    print()

    # --------------------------------------------------------
    # 2. PROPERTY RECOMMENDATION ENGINE
    # --------------------------------------------------------

    print(
        "[2/4] Initializing property recommendation engine..."
    )

    try:
        initialize_recommendations()

        print(
            "      ✓ Recommendation engine initialized."
        )

    except Exception as exc:

        print(
            f"      ✗ Recommendation initialization failed: {exc}"
        )

    print()

    # --------------------------------------------------------
    # 3. GENERATIVE AI
    # --------------------------------------------------------

    print(
        "[3/4] Initializing Generative AI assistant..."
    )

    try:
        initialize_ai()

        print(
            "      ✓ Generative AI initialization completed."
        )

    except Exception as exc:

        print(
            f"      ✗ Generative AI initialization failed: {exc}"
        )

    print()

    # --------------------------------------------------------
    # 4. RAG KNOWLEDGE BASE
    # --------------------------------------------------------

    print(
        "[4/4] Initializing RAG knowledge base..."
    )

    try:
        initialize_rag()

        print(
            "      ✓ RAG knowledge base initialized."
        )

    except Exception as exc:

        print(
            f"      ✗ RAG initialization failed: {exc}"
        )

    print()
    print("=" * 65)
    print("       APPLICATION STARTUP COMPLETED")
    print("=" * 65)
    print()
    print("   API Documentation:")
    print("   http://127.0.0.1:8000/docs")
    print()
    print("   Web Application:")
    print("   http://127.0.0.1:8000")
    print()
    print("=" * 65)
    print()

    yield

    # --------------------------------------------------------
    # APPLICATION SHUTDOWN
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("       AI REAL ESTATE PLATFORM SHUTTING DOWN")
    print("=" * 65)
    print()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Real Estate Intelligence Platform",

    description=(
        "An AI-powered real estate platform combining "
        "machine learning price prediction, property "
        "recommendations, Generative AI and RAG."
    ),

    version="1.0.0",

    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# API ROUTES
# ============================================================

# ------------------------------------------------------------
# Price Prediction
# ------------------------------------------------------------

app.include_router(
    prediction_router,

    prefix="/api/prediction",

    tags=["Price Prediction"],
)


# ------------------------------------------------------------
# Property Recommendation
# ------------------------------------------------------------

app.include_router(
    recommendation_router,

    prefix="/api/recommendation",

    tags=["Property Recommendation"],
)


# ------------------------------------------------------------
# Generative AI Assistant
# ------------------------------------------------------------

app.include_router(
    chatbot_router,

    prefix="/api/chatbot",

    tags=["AI Real Estate Assistant"],
)


# ------------------------------------------------------------
# RAG Knowledge Assistant
# ------------------------------------------------------------

app.include_router(
    rag_router,

    prefix="/api/rag",

    tags=["RAG Knowledge Assistant"],
)


# ============================================================
# STATIC FRONTEND
# ============================================================

app.mount(
    "/static",

    StaticFiles(
        directory=STATIC_DIR
    ),

    name="static",
)


# ============================================================
# HOME PAGE
# ============================================================

@app.get(
    "/",
    tags=["System"]
)
async def home():

    index_file = STATIC_DIR / "index.html"

    return FileResponse(
        index_file
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/api/health",
    tags=["System"]
)
async def health_check():

    return {
        "status": "healthy",

        "application": (
            "AI Real Estate Intelligence Platform"
        ),

        "version": "1.0.0",

        "services": {

            "api": "online",

            "price_prediction": "online",

            "recommendation": "online",

            "ai_assistant": "online",

            "rag": "online",
        },
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get(
    "/api",
    tags=["System"]
)
async def api_information():

    return {
        "application": (
            "AI Real Estate Intelligence Platform"
        ),

        "version": "1.0.0",

        "description": (
            "AI-powered real estate application "
            "for property price prediction, "
            "recommendations, Generative AI and RAG."
        ),

        "features": [
            "ML Price Prediction",
            "Property Recommendation",
            "Generative AI Assistant",
            "RAG Knowledge Assistant",
        ],

        "endpoints": {

            "home": "/",

            "health": "/api/health",

            "prediction": "/api/prediction",

            "recommendation": "/api/recommendation",

            "chatbot": "/api/chatbot",

            "rag": "/api/rag",

            "documentation": "/docs",
        },
    }