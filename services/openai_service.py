import json
from urllib import request
from openai import OpenAI
from django.conf import settings
import requests

# from functions.my_logger import get_request_logger


client = OpenAI(api_key="key_")


def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful senior developer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = settings.OPENROUTER_MODEL

def ask_openai2(prompt):
    # logger, handler = get_request_logger()

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a senior software engineer helping developers."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # logger.info("REQUEST PAYLOAD: %s", json.dumps(payload))

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,     # ✅ let requests handle JSON
            timeout=30
        )
        
        # logger.info("RESPONSE STATUS: %s", response.status_code)
        # logger.info("RESPONSE BODY: %s", response.text.strip())
            
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("bab exception: ", e)
        # logger.error("ERROR: %s", str(e))
        raise
    
    finally:
        print("bab into the final")
        # 🔴 IMPORTANT: prevent handler leak
        # logger.removeHandler(handler)
        # handler.close()

