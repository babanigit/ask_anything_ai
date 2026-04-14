import json
from django.conf import settings
import requests

OPENROUTER_URL = settings.OPENROUTER_URL
MODEL = settings.OPENROUTER_MODEL

CHAT_HISTORY = []
MAX_HISTORY = 10
PAYLOAD_MESSAGE_LENGTH =0

def pp_ask_ai_service(user_question, system_prompt, portfolio_data):

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
 
    CHAT_HISTORY.append({"role": "user", "content": user_question})
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            # *CHAT_HISTORY[-MAX_HISTORY:]
            {"role": "system", "content": f"Portfolio Data (JSON): {json.dumps(portfolio_data)}"},
                        *CHAT_HISTORY[-MAX_HISTORY:]

            # {"role": "user", "content": user_question}
        ]
    }
    
    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload, # let requests handle JSON
            timeout=30
        )

        response.raise_for_status()
        reply_content = response.json()["choices"][0]["message"]["content"]
        CHAT_HISTORY.append({"role": "assistant", "content": reply_content})
        
        PAYLOAD_MESSAGE_LENGTH = len(payload["messages"])

        return reply_content, json.dumps(payload), PAYLOAD_MESSAGE_LENGTH, CHAT_HISTORY

    except Exception as e:
        raise e
    
    # finally:
    #     print("hello aniket into final")
