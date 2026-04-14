from django.urls import path
from .views import pp_view

urlpatterns = [
    path("ask/", pp_view),
]
