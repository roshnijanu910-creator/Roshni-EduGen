from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.schemas import (
    AIResponse,
    AskRequest,
    HealthResponse,
    LearningPathRequest,
    QuizRequest,
    TextRequest,
)
from app.services.gemini_service import GeminiService


# Load application settings
settings = get_settings()


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "EduGenie - Google Gemini powered "
        "learning assistant."
    ),
)


# Serve frontend static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


def run_ai(function, *args):
    """
    Execute an AI service function and convert service
    failures into API-friendly HTTP responses.
    """
    try:
        service = GeminiService(settings)
        return function(service, *args)

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI service error: {exc}",
        ) from exc


# Home page
@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(STATIC_DIR / "index.html")


# Health check
@app.get(
    "/api/health",
    response_model=HealthResponse,
)
async def health():
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
    )


# Ask AI
@app.post(
    "/api/ask",
    response_model=AIResponse,
)
async def ask(request: AskRequest):
    result = run_ai(
        lambda service, question, level:
            service.ask(question, level),
        request.question,
        request.level,
    )

    return AIResponse(
        success=True,
        result=result,
    )


# Summarize text
@app.post(
    "/api/summarize",
    response_model=AIResponse,
)
async def summarize(request: TextRequest):
    result = run_ai(
        lambda service, text:
            service.summarize(text),
        request.text,
    )

    return AIResponse(
        success=True,
        result=result,
    )


# Generate quiz
@app.post(
    "/api/quiz",
    response_model=AIResponse,
)
async def quiz(request: QuizRequest):
    result = run_ai(
        lambda service, topic, count, difficulty, level:
            service.create_quiz(
                topic,
                count,
                difficulty,
                level,
            ),
        request.topic,
        request.count,
        request.difficulty,
        request.level,
    )

    return AIResponse(
        success=True,
        result=result,
    )


# Generate learning path
@app.post(
    "/api/learning-path",
    response_model=AIResponse,
)
async def learning_path(
    request: LearningPathRequest,
):
    result = run_ai(
        lambda service, goal, level, weeks:
            service.learning_path(
                goal,
                level,
                weeks,
            ),
        request.goal,
        request.level,
        request.weeks,
    )

    return AIResponse(
        success=True,
        result=result,
    )


# Get AI recommendations
@app.get(
    "/api/recommend",
    response_model=AIResponse,
)
async def recommend(
    topic: str = Query(
        ...,
        min_length=1,
        max_length=500,
    ),
    level: str = Query(
        default="college",
    ),
):
    topic = topic.strip()
    level = level.strip().lower()

    if not topic:
        raise HTTPException(
            status_code=422,
            detail="Topic cannot be empty.",
        )

    allowed_levels = {
        "school",
        "college",
        "beginner",
        "intermediate",
        "advanced",
    }

    if level not in allowed_levels:
        raise HTTPException(
            status_code=422,
            detail="Invalid learning level.",
        )

    result = run_ai(
        lambda service, topic_value, level_value:
            service.recommendation(
                topic_value,
                level_value,
            ),
        topic,
        level,
    )

    return AIResponse(
        success=True,
        result=result,
    )