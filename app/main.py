import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from .rule_engine import calculate_metrics, detect_patterns
from .llm_service import generate_insight

load_dotenv()

app = Flask(__name__)

@app.route('/api/analyze-activity', methods=['POST'])
def analyze_activity():
    data = request.get_json()
    
    if not data or 'activities' not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid request payload. Expected a JSON object with an 'activities' array."
        }), 400
        
    activities = data.get('activities', [])
    
    if not isinstance(activities, list):
        return jsonify({
            "status": "error",
            "message": "'activities' must be an array."
        }), 400
        
    if not activities:
        return jsonify({
            "status": "success",
            "rule_based_metrics": {
                "total_active_minutes": 0,
                "most_used_app": None,
                "distraction_percentage": 0.0
            },
            "useful_insight": "You haven't logged any activities today. Start working to get some insights!"
        }), 200

    # 1. Rule-based logic
    metrics = calculate_metrics(activities)
    
    # 2. Pattern detection (bridges rule engine and LLM)
    pattern = detect_patterns(metrics)
    
    # 3. LLM logic (receives both metrics and detected pattern)
    insight = generate_insight(metrics, pattern)
    
    # 4. Format output
    return jsonify({
        "status": "success",
        "rule_based_metrics": metrics,
        "pattern_detected": pattern,
        "useful_insight": insight
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
