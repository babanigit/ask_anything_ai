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
    history_str = body.get("history")

    history_json = json.loads(history_str)

    if not user_input:
        return JsonResponse({
            "success": False,
            "message": "No input provided"
        }, status=400)
        
    if history_json is not None and not isinstance(history_json, list):
        return JsonResponse({
            "success": False,
            "message": "History must be a list of message objects"
        }, status=400)
        
    # get prompts -- user and system
    user_prompt = pp_build_dev_prompt(user_input)
    system_prompt= pp_system_prompt()
        
    try:
        # load portfolio data
        portfolio_data, model_name = pp_gist_data()
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to fetch portfolio data: {str(e)}"
        }, status=500)
        
    try:
        response_message, response_history = pp_ask_ai_service(user_prompt, system_prompt, portfolio_data, history_json, model_name) #get service 
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to fetch ai response: {str(e)}"
        }, status=500) 
        
    print("RESPONSE SENDED...")
    return JsonResponse({
        "success": True,
        "message": response_message,
        "history": response_history

    },status=200)


