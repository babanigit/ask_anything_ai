from django.urls import path
from .views import test_api

urlpatterns = [
    path('test/', test_api),
    path('status/', test_api),
]
