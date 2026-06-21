import json
# from urllib import request
# from openai import OpenAI
from django.conf import settings
import requests

# from functions.my_logger import get_request_logger


# client = OpenAI(api_key="key_")


# def ask_openai(prompt):
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful senior developer."},
#             {"role": "user", "content": prompt},
#         ],
#         temperature=0.3,
#     )

#     return response.choices[0].message.content


OPENROUTER_URL = settings.OPENROUTER_URL
MODEL = settings.OPENROUTER_MODEL

MAX_HISTORY = 10

def ask_openai2(prompt, history=None):
    if history is None:
        history = []
    # logger, handler = get_request_logger()

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
 
    history.append({"role": "user", "content": prompt})
    
    # print(f"Current chat history: {history}")  # Debugging line to check chat history
    system_prompt =  history[0]["content"] + " and my name is Aniket, age 23, software developer" if history else "User: Aniket. Full-stack dev. Works with Django, Docker, AI APIs."  # Use the first message as system prompt or default

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            *history[-MAX_HISTORY:]
        ]
    }
    
    try:
        # logger.info("REQUEST PAYLOAD: %s", json.dumps(payload))

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload, # let requests handle JSON
            timeout=30
        )
        
        # logger.info("RESPONSE STATUS: %s", response.status_code)
        # logger.info("RESPONSE BODY: %s", response.text.strip())
            
        response.raise_for_status()
        reply_content = response.json()["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": reply_content})
        
        payload_message_length = len(payload["messages"])

        return reply_content, json.dumps(payload), payload_message_length, history

    except Exception as e:
        print("bab exception: ", e)
        # logger.error("ERROR: %s", str(e))
        raise
    
    finally:
        print("bab into the final")
        # 🔴 IMPORTANT: prevent handler leak
        # logger.removeHandler(handler)
        # handler.close()


