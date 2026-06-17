import requests

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b-instruct"

def query_ollama_judge(system_prompt: str, user_text: str, model: str = OLLAMA_MODEL) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "stream": False,
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()

SYSTEM_PROMPT = """You are an impartial judge.

You are given:
1. Weather forecast data
2. A user question
3. An assistant response

Evaluate how correct and sufficient the assistant response is based ONLY on the forecast data.

Scoring rules (0–10):
- 0–2: Incorrect or contradicted by API response
- 3–5: Partially correct but missing key details
- 6–8: Mostly correct and useful
- 9–10: Fully correct and complete

Return ONLY valid JSON:
{
  "score": <number>,
  "reason": "<short explanation>"
}

Do not add anything else.
"""

def build_judge_input(context, user_query, assistant_response):
    return f"""
    Weather Forecast Data:
    {context}
    
    User Question:
    {user_query}
    
    Assistant Response:
    {assistant_response}
    """.strip()


