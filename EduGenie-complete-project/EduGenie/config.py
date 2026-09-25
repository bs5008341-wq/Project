import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie - Gemini Powered Learning Assistant")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    local_explanation_enabled: bool = _as_bool(
        os.getenv("LOCAL_EXPLANATION_ENABLED"), True
    )
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    demo_mode: bool = _as_bool(os.getenv("DEMO_MODE"), False)
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "12000"))


settings = Settings()
