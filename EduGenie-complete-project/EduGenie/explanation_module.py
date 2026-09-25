from functools import lru_cache

from config import settings
from gemini_client import generate_text
from utils import validate_text


@lru_cache(maxsize=1)
def _get_local_pipeline():
    if not settings.local_explanation_enabled:
        return None

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "transformers is not installed. Install requirements.txt or disable "
            "LOCAL_EXPLANATION_ENABLED."
        ) from exc

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        tokenizer=settings.local_explanation_model,
    )


def _demo_explanation(topic: str) -> str:
    return (
        f"{topic.title()} is a concept that can be understood by breaking it "
        "into smaller ideas. Start with the definition, learn the main parts, "
        "then connect the concept to a simple real-world example."
    )


def explain_concept(text: str) -> str:
    topic = validate_text(text)

    if settings.demo_mode:
        return _demo_explanation(topic)

    if settings.local_explanation_enabled:
        try:
            generator = _get_local_pipeline()
            prompt = (
                "Explain the following educational topic in simple language. "
                "Use short sentences and one small example. Avoid unnecessary jargon.\n\n"
                f"Topic: {topic}"
            )
            result = generator(prompt, max_new_tokens=180, do_sample=False)
            if result and result[0].get("generated_text"):
                return result[0]["generated_text"].strip()
        except Exception:
            # Gemini is a practical fallback if the local model cannot load.
            pass

    return generate_text(
        f"Explain this educational topic in simple language for a beginner:\n\n{topic}",
        system_instruction=(
            "You are EduGenie, an educational tutor. Be concise, accurate, "
            "friendly and beginner-friendly."
        ),
    )
