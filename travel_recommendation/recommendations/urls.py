# recommendations/urls.py

from django.urls import path
from .views import get_recommendations

urlpatterns = [
    path('get-recommendations/', get_recommendations, name='get_recommendations'),
]
