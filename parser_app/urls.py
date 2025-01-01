from django.urls import path
from .views import parse_library, parse_view

urlpatterns = [
    path("", parse_view, name="parse_view"),
    path("parse_library/", parse_library, name="parse_library"),
]
