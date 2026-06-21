from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# from ratelimit.decorators import ratelimit
# from django_ratelimit.decorators import ratelimit
from prompts.dev_prompt import build_dev_prompt
from services.openai_service import ask_openai2


# from django.shortcuts import render

# def frontend(request):
#     return render(request, "index.html")


@csrf_exempt
# @ratelimit(key="ip", rate="5/m", block=True)
def ask_ai(request):
    
    if request.method != "POST":
        return JsonResponse({"success": False,
            "message": "POST only"}, status=405)

    body = json.loads(request.body)

    language = body.get("language")
    intent = body.get("intent")
    user_input = body.get("input")
    history = body.get("history")
    
    if not user_input:
        return JsonResponse({
            "success": False,
            "message": "No input provided"
        }, status=400)

    if history is not None and not isinstance(history, list):
        return JsonResponse({
            "success": False,
            "message": "History must be a list of message objects"
        }, status=400)
        
    # print(f"Received request: language={language}, intent={intent}, input={user_input}")

    prompt = build_dev_prompt(language, intent, user_input) #create prompt
    
    try:
        ai_response, payload, payload_message_length, updated_history = ask_openai2(prompt, history) #get service
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to get AI response: {str(e)}"
        }, status=500)
    
    return JsonResponse({
        "success": True,
        "message_ai_response": ai_response,
        "payload_for_ref": payload,
        "payload_message_length_for_ref": payload_message_length,
        "total_chat_history_for_ref": updated_history
    },status=200)

