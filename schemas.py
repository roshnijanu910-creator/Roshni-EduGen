from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=12000,
        description="Text provided by the user."
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Text cannot be empty.")

        return value


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )

    level: Literal[
        "school",
        "college",
        "beginner",
        "intermediate",
        "advanced"
    ] = "college"

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


class QuizRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    count: int = Field(
        default=5,
        ge=1,
        le=10
    )

    difficulty: Literal[
        "easy",
        "medium",
        "hard"
    ] = "medium"

    level: Literal[
        "school",
        "college",
        "beginner",
        "intermediate",
        "advanced"
    ] = "college"

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Topic cannot be empty.")

        return value


class LearningPathRequest(BaseModel):
    goal: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    weeks: int = Field(
        default=4,
        ge=1,
        le=24
    )

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Learning goal cannot be empty.")

        return value


class AIResponse(BaseModel):
    success: bool = True
    result: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str