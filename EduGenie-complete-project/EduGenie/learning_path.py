from config import settings
from gemini_client import generate_text
from utils import validate_text


def _demo_path(topic: str) -> str:
    return f"""Learning path for {topic}

1. Beginner
- Learn the definition and basic terminology.
- Identify the main components.
- Study one simple example.

2. Intermediate
- Practice common problems and applications.
- Compare related concepts.
- Build a small exercise or project.

3. Advanced
- Study deeper theory and edge cases.
- Read authoritative references.
- Complete a project and review your weak areas.

Suggested resources: textbooks, official documentation, tutorials and practice exercises.
"""


def get_learning_recommendations(topic: str) -> str:
    topic = validate_text(topic)

    if settings.demo_mode:
        return _demo_path(topic)

    return generate_text(
        f"""
Create a personalized learning path for: {topic}

Organize it from beginner to advanced.
For each level include:
- topics/concepts to learn
- practical activities
- a suggested progression

Also suggest useful resource types such as videos, articles, books, documentation,
and practice exercises. Keep the plan realistic and concise.
""".strip(),
        system_instruction=(
            "You are EduGenie, a learning-path designer. Adapt the plan to a learner "
            "starting from fundamentals and progressing toward advanced understanding."
        ),
    )
