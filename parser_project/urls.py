from django.contrib import admin
from django.urls import path
from parser_app.views import parse_library

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parse/', parse_library, name='parse_library'),
    path('', parse_library),  # Пустой маршрут перенаправляет на функцию парсера
]
