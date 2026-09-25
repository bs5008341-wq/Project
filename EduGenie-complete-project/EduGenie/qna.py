from config import settings
from gemini_client import generate_text
from utils import validate_text


def _demo_answer(question: str) -> str:
    return (
        f"Demo answer: {question.strip()} is best understood by identifying "
        "the key concept, its main characteristics, and a simple example. "
        "Add a Gemini API key to receive a model-generated answer."
    )


def answer_question(question: str) -> str:
    question = validate_text(question)

    if settings.demo_mode:
        return _demo_answer(question)

    return generate_text(
        f"Answer the following academic question clearly and concisely:\n\n{question}",
        system_instruction=(
            "You are EduGenie, an academic question-answering assistant. "
            "Give accurate, easy-to-understand answers. If the question is "
            "ambiguous, state the assumption you are making."
        ),
    )
