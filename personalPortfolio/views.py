from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from prompts.personal_portfolio_prompts import pp_build_dev_prompt, pp_system_prompt
from services.personal_portfolio_ai_service import pp_ask_ai_service
from services.get_gists import pp_gist_data

@csrf_exempt
def pp_view(request):    
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST only"
            }, status=405)
    body = json.loads(request.body)
    user_input = body.get("input")
    if not user_input:
        
        return JsonResponse({
            "success": False,
            "message": "No input provided"
        }, status=400)
        
        
    # get prompts -- user and system
    user_prompt = pp_build_dev_prompt(user_input)
    system_prompt= pp_system_prompt()
        
    try:
        # load portfolio data
        portfolio_data = pp_gist_data()
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to fetch portfolio data: {str(e)}"
        }, status=500)
        
    try:
        ai_response, payload, PAYLOAD_MESSAGE_LENGTH, CHAT_HISTORY = pp_ask_ai_service(user_prompt, system_prompt, portfolio_data) #get service 
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to fetch ai response: {str(e)}"
        }, status=500)
        
    
    return JsonResponse({
        "success": True,
        "message": ai_response,
        "payload_for_ref": payload,
        "payload_message_length_for_ref": PAYLOAD_MESSAGE_LENGTH,
        "total_chat_history_for_ref": CHAT_HISTORY
    },status=200)

