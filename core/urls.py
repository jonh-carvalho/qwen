# <project_name>/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aac/', include('aac.urls')),  # Inclui as rotas do app AAC
]
