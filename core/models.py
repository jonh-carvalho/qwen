from django.db import models


class AcademicActivity(models.Model):
    TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    activity_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField()
    hours = models.PositiveIntegerField()
    institution = models.CharField(max_length=255, blank=True, null=True)
    certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title} ({self.activity_type})"
