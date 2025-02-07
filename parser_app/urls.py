#urls.py

from django.urls import path
from .views import parse_library, parse_view, get_authors, author_details, delete_author, analyze_authors

urlpatterns = [
    path("", parse_view, name="parse_view"),
    path("parse_library/", parse_library, name="parse_library"),
    path("get_authors/", get_authors, name="get_authors"),

    path('delete_author/<int:author_id>/', delete_author, name='delete_author'),
    path('author_details/<int:author_id>/', author_details, name='author_details'),

    path('analyze_authors/', analyze_authors, name='analyze_authors'),
]
