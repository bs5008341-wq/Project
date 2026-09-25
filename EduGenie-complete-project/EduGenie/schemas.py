from pydantic import BaseModel, Field, field_validator

from config import settings


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=settings.max_input_chars)


class QuestionRequest(TextRequest):
    count: int = Field(default=3, ge=1, le=10)
