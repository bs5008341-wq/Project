from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import TextRequest, QuestionRequest
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie - Gemini Powered Learning Assistant",
    description="AI learning assistant with Q&A, explanations, quizzes, summaries and learning paths.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "demo_mode": settings.demo_mode,
        "gemini_configured": settings.gemini_api_key is not None,
        "local_explanation_enabled": settings.local_explanation_enabled,
    }


@app.post("/qa")
def qa(payload: TextRequest):
    return {"answer": answer_question(payload.text)}


@app.post("/explain")
def explain(payload: TextRequest):
    return {"explanation": explain_concept(payload.text)}


@app.post("/quiz")
def quiz(payload: QuestionRequest):
    return {"quiz": generate_quiz(payload.text, payload.count)}


@app.post("/summarize")
def summarize(payload: TextRequest):
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
def learning_recommendations(payload: TextRequest):
    return {"learning_path": get_learning_recommendations(payload.text)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
