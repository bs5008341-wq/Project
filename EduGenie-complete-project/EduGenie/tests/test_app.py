from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda text: "Test answer")
    response = client.post("/qa", json={"text": "What is AI?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}


def test_explain(monkeypatch):
    monkeypatch.setattr(main, "explain_concept", lambda text: "Simple explanation")
    response = client.post("/explain", json={"text": "Photosynthesis"})
    assert response.status_code == 200
    assert response.json() == {"explanation": "Simple explanation"}


def test_quiz(monkeypatch):
    expected = [{
        "question": "2+2?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "4",
    }]
    monkeypatch.setattr(main, "generate_quiz", lambda text, count: expected)
    response = client.post("/quiz", json={"text": "Math", "count": 1})
    assert response.status_code == 200
    assert response.json()["quiz"] == expected


def test_summary(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Short summary")
    response = client.post("/summarize", json={"text": "Long passage"})
    assert response.status_code == 200
    assert response.json() == {"summary": "Short summary"}


def test_learning_path(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda text: "Beginner -> Advanced")
    response = client.post("/learn/recommendations", json={"text": "SQL"})
    assert response.status_code == 200
    assert response.json() == {"learning_path": "Beginner -> Advanced"}
