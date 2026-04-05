# aac/urls.py
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import AcademicActivityViewSet

router = DefaultRouter()
router.register(r'activities', AcademicActivityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
