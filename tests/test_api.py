from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "EduGenie"


def test_empty_question_is_rejected():
    response = client.post(
        "/api/ask",
        json={
            "question": "",
            "level": "college"
        }
    )

    assert response.status_code == 422


def test_invalid_quiz_count_is_rejected():
    response = client.post(
        "/api/quiz",
        json={
            "topic": "Python",
            "count": 20,
            "difficulty": "easy",
            "level": "college"
        }
    )

    assert response.status_code == 422


def test_ask_with_mocked_ai(monkeypatch):

    class FakeGeminiService:

        def __init__(self, settings):
            pass

        def ask(self, question, level):
            return (
                f"Answer for {question} "
                f"at {level} level."
            )


    monkeypatch.setattr(
        "app.main.GeminiService",
        FakeGeminiService
    )


    response = client.post(
        "/api/ask",
        json={
            "question": "What is Python?",
            "level": "beginner"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "What is Python?" in data["result"]


def test_learning_path_with_mocked_ai(
    monkeypatch
):

    class FakeGeminiService:

        def __init__(self, settings):
            pass

        def learning_path(
            self,
            goal,
            level,
            weeks
        ):
            return (
                f"Learning path for {goal} "
                f"for {weeks} weeks."
            )


    monkeypatch.setattr(
        "app.main.GeminiService",
        FakeGeminiService
    )


    response = client.post(
        "/api/learning-path",
        json={
            "goal": "Learn Python",
            "level": "beginner",
            "weeks": 4
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "Learn Python" in data["result"]