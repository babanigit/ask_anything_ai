import json
from django.conf import settings
import requests

OPENROUTER_URL = settings.OPENROUTER_URL
# MODEL = settings.OPENROUTER_MODEL

MAX_HISTORY = 10

def pp_ask_ai_service(user_question, system_prompt, portfolio_data, history=None, model_name=settings.OPENROUTER_MODEL):
    if history is None:
        history = []
        
    MODEL = model_name

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    history.append({"role": "user", "content": user_question})
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Portfolio Data (JSON): {json.dumps(portfolio_data)}"},
            *history[-MAX_HISTORY:]
        ]
    }
    
    try:

        response = requests.post(
            str(OPENROUTER_URL),
            headers=headers,
            json=payload, # let requests handle JSON
            timeout=30
        )

        response.raise_for_status()
        reply_content = response.json()["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": reply_content})
        
        # payload_message_length = len(payload["messages"])

        return reply_content ,json.dumps(history)

    except Exception as e:
        raise e

