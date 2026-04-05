# admin.py
from django.contrib import admin

from .models import AcademicActivity


@admin.register(AcademicActivity)
class AcademicActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'date', 'hours', 'institution')
    list_filter = ('activity_type', 'date')
    search_fields = ('title', 'description')
