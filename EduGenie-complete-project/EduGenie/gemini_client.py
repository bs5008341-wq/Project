from functools import lru_cache

from config import settings


@lru_cache(maxsize=1)
def get_gemini_client():
    from google import genai

    if not settings.gemini_api_key:
        raise RuntimeError(
            "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    json_mode: bool = False,
) -> str:
    client = get_gemini_client()

    from google.genai import types

    config_kwargs = {}
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction
    if json_mode:
        config_kwargs["response_mime_type"] = "application/json"

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
