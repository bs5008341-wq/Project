# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant based on the project documentation. It provides:

- Q&A
- Simple concept explanations
- Three or more generated MCQs with four options
- Educational passage summarization
- Personalized learning paths

The documented architecture uses FastAPI for the backend, HTML/CSS for the frontend, Gemini for Q&A/summarization/quiz/learning paths, and LaMini-Flan-T5 for concept explanations.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── utils.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## 1. Open in VS Code

1. Extract/open the `EduGenie` folder in VS Code.
2. Install Python 3.10+.
3. Open **Terminal → New Terminal**.

## 2. Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> The LaMini model is downloaded from Hugging Face the first time the explanation module loads it, so the first explanation request may take longer.

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
DEMO_MODE=false
LOCAL_EXPLANATION_ENABLED=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

Do not commit `.env`. The `.gitignore` already excludes it.

The documentation recommends environment variables for API keys and says not to expose keys in client-side code. This implementation follows that pattern.

## 5. Run without a Gemini key (optional)

For UI/API testing before configuring Gemini:

```text
DEMO_MODE=true
```

Then start the server. Q&A, summary, quiz and learning-path responses use deterministic demo responses. The real Gemini integration is used when `DEMO_MODE=false` and a valid key is configured.

## 6. Start the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The project documentation specifies the same Uvicorn command and local URL.

## 7. Test the API

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Q&A:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Which is the largest ocean?\"}"
```

Explanation:

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Pythagoras theorem\"}"
```

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Photosynthesis\",\"count\":3}"
```

Summary:

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Paste a long educational passage here.\"}"
```

Learning path:

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"SQL\"}"
```

## 8. Run automated tests

```bash
pytest -q
```

The tests mock AI module calls, so they do not require a Gemini API key or a downloaded local model.

## API routes

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health/configuration check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Simple concept explanation |
| POST | `/quiz` | MCQ generation |
| POST | `/summarize` | Text summarization |
| POST | `/learn/recommendations` | Personalized learning path |

## Security

- Keep `GEMINI_API_KEY` only on the server.
- Never put the key in HTML, JavaScript or CSS.
- Never commit `.env`.
- For production, use a managed secret store and API-key restrictions.
- Add authentication/rate limiting before exposing the service publicly.

## Troubleshooting

### `ModuleNotFoundError`

Activate `.venv` and run:

```bash
pip install -r requirements.txt
```

### Gemini authentication error

Check:

```text
GEMINI_API_KEY=...
```

in `.env`, then restart Uvicorn.

### LaMini model fails to load

Set:

```text
LOCAL_EXPLANATION_ENABLED=false
```

The explanation module will then use Gemini as its fallback.

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Documentation alignment

The supplied project document specifies the module layout, FastAPI REST endpoints, HTML task dropdown, textarea and submit button, responsive CSS, live POST integration, and local Uvicorn workflow. This implementation preserves those requirements while completing the missing application code and using the current Google GenAI Python SDK for Gemini calls.
