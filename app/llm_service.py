import os
import google.generativeai as genai

def generate_insight(metrics):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY is not set. Please set it in your .env file."
        
    genai.configure(api_key=api_key)
    
    # Use gemma-4-31b-it (Open Weights) which has free tier availability on this API key
    model = genai.GenerativeModel('gemma-4-31b-it')
    
    prompt = f"""
    You are an expert productivity coach for software engineers. The user spent a total of {metrics.get('total_active_minutes')} minutes active today. 
    Their most used app was {metrics.get('most_used_app')}. 
    Their distraction percentage (time spent on non-work apps) was {metrics.get('distraction_percentage')}%. 
    
    Based on this data, provide a 2-3 sentence genuinely useful observation or piece of advice that they could not immediately see on their own.
    Do not just state the numbers back to them. Be professional, concise, and do not use markdown formatting.
    CRITICAL: Output ONLY the final 2-3 sentence advice. Do NOT include any of your reasoning, thinking process, constraints, or drafts. Start directly with the advice.
    """
    
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
        return f"Error generating insight: {str(e)}"
