# DevHabit Tracker

**A stateless, AI-powered API that transforms raw developer activity logs into actionable productivity insights.**

## Table of contents

- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Philosophy](#philosophy)

## Overview

Millions of people generate data about their digital habits every day. DevHabit Tracker is a backend system designed to ingest a stream of developer activity logs, find behavioral patterns, and deliver a "genuinely useful" observation using a combination of Rule-Based Mathematics and Large Language Models (LLMs).

By correlating hard metrics (e.g., total active time, distraction percentages) with an LLM's analytical reasoning, the API provides personalized productivity coaching that a user might not immediately notice on their own.

## Features

- Hybrid Analysis Engine using deterministic Python logic and Google Gemini API
- Pattern Detection with 5 behavioral classifications and human-readable evidence
- 4-step pipeline: `Data → Metrics → Pattern Detection → LLM Insight`
- Stateless Architecture for zero-setup execution
- Containerized via Docker

## Architecture

```
POST /api/analyze-activity
        │
        ▼
┌─────────────────────┐
│  rule_engine.py      │
│  calculate_metrics() │  ← Pure Python math (no LLM)
│  detect_patterns()   │  ← Classifies behavior with evidence
└────────┬────────────┘
         ▼
┌─────────────────────┐
│  llm_service.py      │
│  generate_insight()  │  ← Gemini API explains the pattern
└────────┬────────────┘
         ▼
    JSON Response

## Installation

This project is built using Python 3.11 and Flask. 

Before installing, ensure you have [Docker](https://docs.docker.com/get-docker/) installed. Alternatively, you can run this locally using [Python](https://www.python.org/downloads/).

You will need a Google Gemini API key to run the LLM engine.
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. In the root directory of this project, create a file named `.env`.
3. Add your key to the file exactly like this:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

## Quick Start

The quickest way to get started is to use Docker.

Clone the repository:
```bash
git clone <your-repository-url>
cd DevhabitTracker
```

Build and start the container:
```bash
docker-compose up --build -d
```

The API will now be running at `http://localhost:5001`.

<details>
<summary>Running Locally with Python</summary>

If you do not have Docker installed, you can run the app directly:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
python -m flask run --port=5001
```
</details>

## Examples

The repository includes a `sample_activity.json` file for easy testing. While the server is running, you can test the `POST /api/analyze-activity` endpoint.

### Using cURL (Linux / macOS)

```bash
curl -X POST http://localhost:5001/api/analyze-activity \
  -H "Content-Type: application/json" \
  -d @sample_activity.json
```

### Using PowerShell (Windows)

```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/analyze-activity" -Method Post -ContentType "application/json" -Body (Get-Content sample_activity.json -Raw) | ConvertTo-Json -Depth 5
```

### Expected JSON Response

```json
{
    "status": "success",
    "rule_based_metrics": {
        "total_active_minutes": 205,
        "most_used_app": "VS Code",
        "distraction_percentage": 34.15,
        "context_switches": 6,
        "focus_sessions": 3,
        "average_focus_duration": 45.0,
        "longest_focus_session": 115
    },
    "pattern_detected": {
        "type": "high_distraction",
        "evidence": [
            "34.15% of active time spent on non-work apps",
            "Only 65.8% of session was productive"
        ]
    },
    "useful_insight": "Your productivity loss is caused by prolonged off-task loops following a single transition rather than frequent multitasking. Install a website blocker with timed intervals to prevent isolated shifts from becoming extended detours."
}
```

## Philosophy

### Why Stateless? (No Database)
The assignment brief prioritized making the system easily runnable by a reviewer. Introducing a persistent database layer (like PostgreSQL) requires schema migrations, volume management, and potential networking issues within Docker. By keeping the API stateless, the trade-off is losing historical tracking across sessions, but the massive benefit is a 100% reliable, zero-friction execution experience for evaluation.

### Future Improvements
If given more time, the following systems would be implemented:
- **Persistent Storage**: To allow tracking habits over long periods without requiring the client to send the entire historical payload on every request.
- **User Authentication**: To securely silo user data in a multi-tenant environment.
- **Asynchronous Processing**: Offloading the LLM API call to a background worker (Celery/Redis) to prevent HTTP thread blocking.
- **Frontend Dashboard**: A React interface to visualize the rule-based metrics with charts.

---
Developed for the Engineering Internship Assessment.
