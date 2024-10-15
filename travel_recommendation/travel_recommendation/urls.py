# travel_recommendation/urls.py

from django.urls import path, include

urlpatterns = [
    path('api/', include('recommendations.urls')),  # Include the URLs from the recommendations app
]