import json
from django.conf import settings
import requests

OPENROUTER_URL = settings.OPENROUTER_URL
MODEL = settings.OPENROUTER_MODEL

CHAT_HISTORY = []
MAX_HISTORY = 10
PAYLOAD_MESSAGE_LENGTH =0

def ask_pp_ai(user_question, portfolio_data):

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
 
    CHAT_HISTORY.append({"role": "user", "content": user_question})
    
    # print(f"Current chat history: {CHAT_HISTORY}")  # Debugging line to check chat history
    
    system_prompt = """
        You are an AI assistant representing Aniket Panchal on his personal portfolio website.

        Your role is to answer questions strictly about Aniket’s:

        - Education
        - Certifications
        - Skills
        - Work experience
        - Technical projects
        - Technologies used
        - Architecture decisions
        - Professional background

        You will be given structured portfolio data in JSON format.

        Rules:

        1. Answer ONLY using the provided portfolio data.
        2. Do NOT generate information that is not present.
        3. If information is missing, respond:
        "That information is not available in the portfolio."
        4. If the question is unrelated to Aniket’s professional background, respond:
        "I’m here to answer questions specifically about Aniket Panchal’s professional profile."
        5. Keep answers concise, professional, and technically clear.
        6. When explaining projects, mention:
        - Tech stack
        - Key features
        - Performance improvements (if available)
        7. Do not answer general knowledge questions.

        Never invent skills, experience, or achievements.
    """

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
