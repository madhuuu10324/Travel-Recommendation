from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=255)
    weather = models.CharField(max_length=50)
    destination_type = models.CharField(max_length=50)
    cost_per_person = models.FloatField()
    places_covered = models.TextField()
    hotel_details = models.TextField()

class Recommendation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    score = models.FloatField()  # A score based on filtering
