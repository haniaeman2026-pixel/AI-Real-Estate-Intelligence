import os
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Real Estate Assistant for an AI-powered
Real Estate Intelligence Platform.

Your job is to help users understand real estate properties,
property prices, property features, market concepts,
investment considerations, and general buying guidance.

Rules:

1. Give clear and practical answers.
2. Use simple professional language.
3. Explain real-estate terminology when necessary.
4. Do not invent specific property facts.
5. Do not claim that a property is definitely a good investment.
6. When discussing financial or legal matters, explain that
   users should verify important decisions with qualified
   professionals.
7. If the user asks about this application's ML prediction,
   explain that predictions are estimates based on the
   available historical dataset.
8. The application uses the Ames Housing Dataset for its
   machine-learning price prediction component.
9. Do not pretend that the dataset represents live market
   prices.
10. If information is unavailable, clearly say so.
"""


# ============================================================
# CLIENT
# ============================================================

client = None


def initialize_ai():

    global client

    if not GROQ_API_KEY:
        print(
            "GROQ_API_KEY not found. "
            "AI assistant will use fallback mode."
        )

        client = None

        return

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    print(
        f"Generative AI initialized using {MODEL_NAME}"
    )


# ============================================================
# STATUS
# ============================================================

def ai_status():

    return {
        "feature": "Generative AI Real Estate Assistant",

        "status": (
            "online"
            if client is not None
            else "fallback"
        ),

        "model": MODEL_NAME,

        "provider": "Groq",
    }


# ============================================================
# FALLBACK ASSISTANT
# ============================================================

def fallback_response(message: str):

    message_lower = message.lower()

    if "price" in message_lower:

        return (
            "Property prices depend on factors such as "
            "location, living area, property quality, "
            "year built, bedrooms, bathrooms and other "
            "features. The ML component of this platform "
            "provides an estimated price using historical "
            "Ames Housing Dataset data."
        )

    if (
        "buy" in message_lower
        or "buying" in message_lower
    ):

        return (
            "When evaluating a property, consider your "
            "budget, location, property condition, size, "
            "bedrooms, bathrooms, neighborhood and "
            "future requirements. Important legal and "
            "financial decisions should be verified with "
            "qualified professionals."
        )

    if (
        "invest" in message_lower
        or "investment" in message_lower
    ):

        return (
            "Real estate investment decisions should "
            "consider purchase price, location, rental "
            "potential, maintenance costs, taxes, "
            "market conditions and long-term goals."
        )

    return (
        "I can help you with property prices, property "
        "features, recommendations, real-estate concepts, "
        "buying guidance and general investment considerations."
    )


# ============================================================
# CHAT FUNCTION
# ============================================================

def chat(message: str):

    global client

    if client is None:
        initialize_ai()

    # --------------------------------------------------------
    # Fallback mode
    # --------------------------------------------------------

    if client is None:

        return {
            "success": True,

            "mode": "fallback",

            "model": MODEL_NAME,

            "answer": fallback_response(
                message
            ),
        }

    # --------------------------------------------------------
    # Groq AI
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],

            temperature=0.3,

            max_tokens=700,
        )

        answer = response.choices[0].message.content

        return {
            "success": True,

            "mode": "generative_ai",

            "provider": "Groq",

            "model": MODEL_NAME,

            "answer": answer,
        }

    except Exception as exc:

        return {
            "success": False,

            "mode": "error",

            "model": MODEL_NAME,

            "answer": (
                "The AI assistant could not process "
                "the request right now."
            ),

            "error": str(exc),
        }