# qa/urls.py

from django.urls import path
from .views import train, question

urlpatterns = [
    path('train/', train, name='train'),
    path('question/', question, name='question')
]
