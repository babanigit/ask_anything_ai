# import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def test_api(request):
    if request.method == "GET":
        # time.sleep(5)   # 5 seconds

        return JsonResponse({
            "status": True,
            "message": "Success"
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
