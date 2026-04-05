# views.py
from rest_framework import viewsets

from .models import AcademicActivity
from .serializers import AcademicActivitySerializer


class AcademicActivityViewSet(viewsets.ModelViewSet):
    queryset = AcademicActivity.objects.all()
    serializer_class = AcademicActivitySerializer
