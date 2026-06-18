# Project Requirements Document (PRD): DevHabit Tracker

## 1. Project Overview and Objectives
**Project Name:** DevHabit Tracker
**Objective:** Build a stateless, containerized backend API endpoint that ingests a stream of developer activity logs, finds patterns using rule-based logic, and leverages an LLM to provide a "genuinely useful" and personalized productivity insight.
**Timeframe:** 24-hour turnaround (6-8 hours execution).

## 2. Technology Stack
- **Backend Framework:** Python & Flask (Lightweight REST API)
- **AI Integration:** Google Gemini API (`google-generativeai`)
- **Database:** None (Stateless API to ensure zero-friction local execution for the reviewer)
- **Infrastructure:** Docker & Docker Compose

## 3. API Specifications
### Endpoint
`POST /api/analyze-activity`

### Request Schema
Accepts a JSON array of daily digital habit objects.
```json
{
  "activities": [
    {"timestamp": "2026-06-18T09:00:00", "app": "VS Code", "duration_minutes": 120},
    {"timestamp": "2026-06-18T11:00:00", "app": "Twitter", "duration_minutes": 45},
    {"timestamp": "2026-06-18T11:45:00", "app": "GitHub", "duration_minutes": 30}
  ]
}
```

### Response Schema
```json
{
  "status": "success",
  "rule_based_metrics": {
    "total_active_minutes": 195,
    "most_used_app": "VS Code",
    "distraction_percentage": 23.0
  },
  "useful_insight": "Your longest coding stretches are consistently followed by high social media usage, suggesting mental fatigue. Try breaking your 120-minute coding blocks into two 60-minute sessions."
}
```

## 4. Rule-Based Engine (Logic Formulas)
A Python function will parse the payload and calculate the following metrics:
1. **`total_active_minutes`**: Sum of all `duration_minutes` in the array.
2. **`most_used_app`**: The application name with the highest cumulative `duration_minutes`.
3. **`distraction_percentage`**: `(Total time on non-work apps / total_active_minutes) * 100`. 
   *(Note: A predefined set of "work" apps (e.g., VS Code, GitHub, Terminal) and "non-work" apps (e.g., Twitter, YouTube, Reddit) will be used to classify the data).*

## 5. LLM Engine & Prompt Structure
- **Integration:** Google Gemini API.
- **Prompt Construction:** A static template that injects the calculated metrics.
- **Prompt Example:**
  > "You are an expert productivity coach for software engineers. The user spent a total of {total_active_minutes} minutes active today. Their most used app was {most_used_app}. Their distraction percentage (time spent on non-work apps) was {distraction_percentage}%. Look at this data and provide a 2-3 sentence 'genuinely useful' observation or piece of advice that the user could not immediately see on their own. Keep it professional and concise."

## 6. Infrastructure and Deployment
- **Dockerization:** A standard `Dockerfile` to containerize the Flask application.
- **Docker Compose:** A `docker-compose.yml` file to expose port 5000 and run the service.
- **Setup for Reviewer:**
  1. Add Google Gemini API key to a `.env` file.
  2. Run `docker-compose up --build`.
  3. Send a POST request to `http://localhost:5000/api/analyze-activity`.

## 7. Deliverables & Roadmap
1. **Phase 1 (1 hour):** Repository Setup (Git, Python virtual environment, dependencies).
2. **Phase 2 (2 hours):** Core API Logic (Flask endpoint and rule-based calculations).
3. **Phase 3 (1.5 hours):** LLM Integration (Connect to Gemini API, format prompt, process response).
4. **Phase 4 (2 hours):** Containerization (Write `Dockerfile` and `docker-compose.yml`).
5. **Phase 5 (1.5 hours):** Documentation (Write an exacting `README.md` and the 200-word decision note).
