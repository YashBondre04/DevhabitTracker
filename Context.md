# Micro-Detailed Project Context

## Project State
**Phase:** Initialization / Scoping
**Core Concept:** DevHabit Tracker (Stateless Activity Analysis API)

## Strict Guardrails (DO NOT BUILD)
- **NO Frontend/UI:** No React, HTML, CSS. Reviewer will use Postman/cURL.
- **NO Database:** No PostgreSQL, Supabase, SQLite. The API must remain fully stateless.
- **NO User Authentication:** No login, JWTs, sessions. Assume single anonymous user.
- **NO Background Jobs:** Process requests synchronously. No Celery/Redis.

## Planned Directory Structure
```text
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                  # Excluded from version control; holds API key
├── README.md             # Execution instructions and future improvements
├── DECISION_NOTE.md      # 200-word explanation of architectural trade-offs
└── app/
    ├── __init__.py
    ├── main.py           # Flask server and route definitions
    ├── rule_engine.py    # Python functions for math/aggregation
    └── llm_service.py    # Gemini API prompt formatting and calling
```

## Environment Variables
- `GEMINI_API_KEY`: Required for Google Gemini API authentication. Must be loaded via `python-dotenv`.

## Dependencies (`requirements.txt` targets)
- `Flask==3.0.3` (or latest stable)
- `google-generativeai==0.5.4` (or latest stable)
- `python-dotenv==1.0.1`

## Detailed Logic Flow Sequence
1. **Request Reception:** Reviewer triggers `POST /api/analyze-activity` with a JSON body.
2. **Validation:** Flask checks if `activities` exists and is a valid array in the JSON payload. Returns 400 if invalid.
3. **Rule Math Parsing:** `rule_engine.py` processes the array:
   - Sums all `duration_minutes` (`total_active_minutes`).
   - Groups by `app` to find the max duration (`most_used_app`).
   - Categorizes apps into work/distraction to calculate `distraction_percentage`.
4. **LLM Invocation:** `llm_service.py` receives the 3 metrics. It injects them into the static prompt template and calls the Gemini API (synchronously).
5. **Response Construction:** The backend awaits the LLM response text, combines it with the rule-based metrics into a final JSON dictionary, and returns it with HTTP 200.
