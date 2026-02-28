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
    
    if not user_input:
        return JsonResponse({
            "success": False,
            "message": "No input provided"
        }, status=400)
        
    print(f"Received request: language={language}, intent={intent}, input={user_input}")

    prompt = build_dev_prompt(language, intent, user_input) #create prompt
    
    # ai_response = ask_openai2(prompt) #get service
    
    # testing response
    ai_response = "Explanation:\nList comprehension is a concise way to create lists in Python. It allows you to generate a new list by applying an expression to each element in an existing iterable, optionally filtering elements based on a condition. List comprehensions provide a more readable and efficient alternative to using loops and appending to a list.\n\nThe general syntax of a list comprehension is:\n```python\nnew_list = [expression for item in iterable if condition]\n```\n\nCode:\n```python\n# Example 1: Squaring numbers in a list\nnumbers = [1, 2, 3, 4, 5]\nsquared_numbers = [x**2 for x in numbers]\nprint(squared_numbers)  # Output: [1, 4, 9, 16, 25]\n\n# Example 2: Filtering even numbers\neven_numbers = [x for x in range(10) if x % 2 == 0]\nprint(even_numbers)  # Output: [0, 2, 4, 6, 8]\n\n# Example 3: Flattening a nested list\nnested_list = [[1, 2], [3, 4], [5, 6]]\nflattened_list = [item for sublist in nested_list for item in sublist]\nprint(flattened_list)  # Output: [1, 2, 3, 4, 5, 6]\n```\n\nTips:\n- Use list comprehensions for simple transformations and filtering operations.\n- Keep the expressions inside list comprehensions concise and readable.\n- Consider using generator expressions instead of list comprehensions when dealing with large datasets to save memory.\n- Avoid using list comprehensions for complex logic; use regular loops instead for better readability."
    
    return JsonResponse({
        "success": True,
        "message": ai_response
    },status=200)
