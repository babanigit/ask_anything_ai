from django.urls import path
from .views import ask_pp_view

urlpatterns = [
    path("ask/", ask_pp_view),
]
