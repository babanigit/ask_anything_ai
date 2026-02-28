from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def test_api(request):
    if request.method == "GET":
        return JsonResponse({
            "status": "success",
            "message": "GET API working 🚀"
        })

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            return JsonResponse({
                "status": "success",
                "received": body
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
