from config import settings
from gemini_client import generate_text
from utils import parse_json, validate_text


def _demo_quiz(topic: str, count: int) -> list[dict]:
    return [
        {
            "question": f"What is the main idea to study first when learning {topic}?",
            "options": [
                "The basic definition",
                "Only advanced formulas",
                "Unrelated historical facts",
                "Random examples",
            ],
            "correct_answer": "The basic definition",
        }
        for _ in range(count)
    ]


def _normalise_quiz(data, count: int) -> list[dict]:
    if isinstance(data, dict):
        data = data.get("questions", data.get("quiz", []))

    if not isinstance(data, list):
        raise ValueError("Quiz response must contain a list of questions.")

    questions = []
    for item in data[:count]:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(
            item.get("correct_answer", item.get("answer", ""))
        ).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            continue
        options = [str(x).strip() for x in options]
        if not all(options) or not answer:
            continue

        questions.append(
            {
                "question": question,
                "options": options,
                "correct_answer": answer,
            }
        )

    if len(questions) < count:
        raise ValueError("Gemini returned an incomplete quiz.")
    return questions


def generate_quiz(text: str, count: int = 3) -> list[dict]:
    text = validate_text(text)
    count = max(1, min(int(count), 10))

    if settings.demo_mode:
        return _demo_quiz(text, count)

    prompt = f"""
Create exactly {count} multiple-choice questions from the educational text below.

Return ONLY valid JSON in this shape:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "One exact option from options"
    }}
  ]
}}

Rules:
- Exactly four options per question.
- Exactly one correct answer.
- Questions must be answerable from the supplied text/topic.
- Make distractors plausible.
- Do not include Markdown or explanations.

Educational text/topic:
{text}
""".strip()

    raw = generate_text(
        prompt,
        system_instruction=(
            "You generate educational MCQs and must follow the requested JSON structure exactly."
        ),
        json_mode=True,
    )
    return _normalise_quiz(parse_json(raw), count)
