from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from prompts.dev_prompt import build_dev_prompt
from services.personal_portfolio_ai_service import ask_pp_ai
from services.get_gists import fetch_gist_file, load_portfolio_data


@csrf_exempt
def ask_pp_view(request):    
    if request.method != "POST":
        return JsonResponse({"success": False,
            "message": "POST only"}, status=405)
    body = json.loads(request.body)
    user_input = body.get("input")
    if not user_input:
        
        return JsonResponse({
            "success": False,
            "message": "No input provided"
        }, status=400)
        
    prompt = build_dev_prompt(user_input) #create prompt
        
    try:
        
        portfolio_data = load_portfolio_data()
        # print(f"Fetched portfolio data: {portfolio_data}")  # Debugging line to check fetched data 

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Failed to fetch portfolio data: {str(e)}"
        }, status=500)
        
    ai_response,payload, PAYLOAD_MESSAGE_LENGTH , CHAT_HISTORY = ask_pp_ai(prompt, portfolio_data) #get service
    
    return JsonResponse({
        "success": True,
        "message_ai_response": ai_response,
        "payload_for_ref": payload,
        "payload_message_length_for_ref": PAYLOAD_MESSAGE_LENGTH,
        "total_chat_history_for_ref": CHAT_HISTORY
    },status=200)
