# qa/models.py

from django.db import models

class DocumentVector(models.Model):
    text = models.TextField()
    vector = models.JSONField()  # Stores vectors as JSON arrays
