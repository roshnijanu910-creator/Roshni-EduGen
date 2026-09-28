from typing import Optional

from app.config import Settings


SYSTEM_INSTRUCTION = """
You are EduGenie, a friendly and reliable educational AI assistant.

Your job is to help students understand subjects clearly.

Rules:
1. Give accurate educational information.
2. Explain difficult concepts in simple language.
3. Adjust explanations according to the student's level.
4. Use headings, bullet points, examples, and steps when useful.
5. Do not invent facts, sources, citations, links, or references.
6. If something is uncertain, clearly say so.
7. Keep answers focused on the student's request.
8. For programming questions, provide correct and readable code when appropriate.
9. For quizzes, clearly separate questions, options, and answers.
10. Encourage learning rather than simply giving unexplained answers.
"""


class GeminiService:
    """
    Service responsible for communicating with Google's Gemini API.

    The Google SDK is imported lazily so that API tests that do not
    make a real Gemini request can run without requiring the SDK to
    initialize.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Create a .env file and add your Gemini API key."
            )

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "The google-genai package is not installed. "
                "Run: pip install -r requirements.txt"
            ) from exc

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.4
    ) -> str:

        from google.genai import types

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )

        text: Optional[str] = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    def ask(
        self,
        question: str,
        level: str
    ) -> str:

        prompt = f"""
Student level: {level}

Student question:
{question}

Answer the question in a way that is appropriate for the student's level.

Structure the response with:
- Direct answer
- Explanation
- Example if useful
- Important points

Do not make the answer unnecessarily complicated.
"""

        return self.generate(prompt)

    def summarize(self, text: str) -> str:

        prompt = f"""
Summarize the following educational text.

Requirements:
- Identify the main idea.
- Keep important facts.
- Remove unnecessary repetition.
- Use simple language.
- Use bullet points where useful.
- Do not add information that is not present in the original text.

Text:

{text}
"""

        return self.generate(prompt)

    def create_quiz(
        self,
        topic: str,
        count: int,
        difficulty: str,
        level: str
    ) -> str:

        prompt = f"""
Create a quiz for a student.

Topic: {topic}
Number of questions: {count}
Difficulty: {difficulty}
Student level: {level}

For every question provide:

Question:
A)
B)
C)
D)

Correct Answer:
Explanation:

Make sure there are exactly {count} questions.

Use clear educational language.
"""

        return self.generate(prompt)

    def learning_path(
        self,
        goal: str,
        level: str,
        weeks: int
    ) -> str:

        prompt = f"""
Create a personalized learning path.

Learning goal:
{goal}

Current level:
{level}

Available duration:
{weeks} weeks

Create a practical weekly learning plan.

For each week include:
1. Topics to learn
2. Learning objectives
3. Practice activities
4. Suggested project or exercise
5. A simple checkpoint

Keep the plan realistic and progressive.
"""

        return self.generate(prompt)

    def recommendation(
        self,
        topic: str,
        level: str
    ) -> str:

        prompt = f"""
Recommend learning resources and activities for:

Topic: {topic}
Student level: {level}

Provide:
- Topics to study first
- Important concepts
- Practice activities
- Small project ideas
- Suggested next steps

Do not invent specific websites, links, books, or courses.
"""

        return self.generate(prompt)