# serializers.py
from rest_framework import serializers
from .models import AcademicActivity

class AcademicActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicActivity
        fields = '__all__'