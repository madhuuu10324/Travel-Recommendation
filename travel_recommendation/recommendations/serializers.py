# recommendations/serializers.py

from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'weather', 'destination_type', 'cost_per_person', 'places_covered', 'hotel_details']
