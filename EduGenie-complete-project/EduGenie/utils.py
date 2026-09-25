import json
import re

from config import settings


def validate_text(text: str) -> str:
    text = (text or "").strip()
    if not text:
        raise ValueError("Input text cannot be empty.")
    if len(text) > settings.max_input_chars:
        raise ValueError(
            f"Input is too long. Maximum allowed length is {settings.max_input_chars} characters."
        )
    return text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_json(text: str):
    cleaned = clean_json_block(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Recover the first JSON object/array when a model adds extra prose.
        first_obj = cleaned.find("{")
        first_arr = cleaned.find("[")
        starts = [x for x in (first_obj, first_arr) if x >= 0]
        if not starts:
            raise
        start = min(starts)
        last_obj = cleaned.rfind("}")
        last_arr = cleaned.rfind("]")
        end = max(last_obj, last_arr)
        if end <= start:
            raise
        return json.loads(cleaned[start : end + 1])
