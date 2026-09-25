from config import settings
from gemini_client import generate_text
from utils import validate_text


def _demo_summary(text: str) -> str:
    words = text.split()
    preview = " ".join(words[:70])
    return (
        f"Demo summary: {preview}"
        + ("..." if len(words) > 70 else "")
        + " Add a Gemini API key for AI-generated summarization."
    )


def summarize_text(text: str) -> str:
    text = validate_text(text)

    if settings.demo_mode:
        return _demo_summary(text)

    return generate_text(
        f"Summarize the following educational passage in simple language. "
        f"Keep the core facts and remove repetition.\n\n{text}",
        system_instruction=(
            "You are an educational summarizer. Produce a concise, clear summary "
            "that preserves important information."
        ),
    )
