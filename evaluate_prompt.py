import requests
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = "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"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

def call_openrouter(system_msg, user_msg):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    }
    response = requests.post(URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def evaluate_prompt(user_prompt):
    system_message = """
You are a prompt evaluation expert. Given a user prompt, score it 1–5 for each of the following:
- Clarity
- Specificity
- Context Provided
- Creativity
- Relevance
- Ambiguity (1 = clear, 5 = very ambiguous)

Then return JSON like:
{
  "clarity": 4,
  "specificity": 3,
  "context": 2,
  "creativity": 3,
  "relevance": 5,
  "ambiguity": 2,
  "total_score": 20,
  "issues": "...",
  "suggestions": "..."
}
    """
    reply = call_openrouter(system_message, user_prompt)
    try:
        json_obj = re.search(r'\{.*\}', reply, re.DOTALL).group()
        return json.loads(json_obj)
    except:
        return {"error": "Could not parse response", "details": reply}

def improve_prompt(user_prompt):
    system_message = """
You are a prompt engineer. Given a user prompt, improve it by increasing clarity, specificity, and relevance. Return only the improved prompt as plain text, without explanation.
    """
    return call_openrouter(system_message, user_prompt)

def compare_prompts(original, improved):
    system_message = """
You are a prompt quality reviewer. Compare the two prompts given below. Briefly explain which one is better and why.
    """
    comparison = f"Original Prompt:\n{original}\n\nImproved Prompt:\n{improved}"
    return call_openrouter(system_message, comparison)
