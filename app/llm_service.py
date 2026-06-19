import os
import google.generativeai as genai
import logging

def _build_prompt(metrics, pattern):
    """
    Constructs the analytical prompt for the LLM. 
    Isolated from the execution logic to ensure maintainability of prompt engineering.
    """
    evidence_list = chr(10).join('- ' + e for e in pattern.get('evidence', []))
    hours_active = round(metrics.get('total_active_minutes', 0) / 60, 1)
    
    return f"""You are a productivity analyst for software engineers. A rule-based system detected a "{pattern.get('type')}" pattern in a user's work session.

Evidence:
{evidence_list}

Supporting data:
- {metrics.get('context_switches')} context switches across {hours_active} hours
- Longest uninterrupted focus block: {metrics.get('longest_focus_session')} minutes
- Average focus session: {metrics.get('average_focus_duration')} minutes
- Most used app: {metrics.get('most_used_app')}

Correlate the evidence with the context switches and focus duration to explain a behavioral cause the user cannot see by looking at raw numbers alone. Then suggest one specific, actionable change. Write exactly 2 sentences. Do not repeat percentages or restate the data. No markdown.
CRITICAL: Output ONLY the 2 sentences. No thinking, no drafts, no preamble."""

def generate_insight(metrics, pattern):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY is not set. Please set it in your .env file."
        
    genai.configure(api_key=api_key)
    
    # Use gemma-4-31b-it (Open Weights) which has free tier availability on this API key
    model = genai.GenerativeModel('gemma-4-31b-it')
    
    prompt = _build_prompt(metrics, pattern)
    
    try:
        response = model.generate_content(prompt)
        insight_text = response.text.strip()
        
        # Open Weights models often output internal "thinking" drafts.
        # We slice it to return ONLY the final generated paragraph.
        lines = [line.strip() for line in insight_text.split('\n') if line.strip()]
        if lines:
            insight_text = lines[-1]
            
        return insight_text
        
    except Exception as e:
        logging.error(f"LLM Generation failed: {e}")
        return "Insight generation is currently unavailable. Please review your raw metrics."
