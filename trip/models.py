from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator


class TripModel(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                              related_name="TripModel_owner")
    trip_img = models.ImageField(upload_to='trip_img', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city


class NoteModel(models.Model):
    EXCURSIONS = (
        ("event", "Event"),
        ("dining", "Dining"),
        ("experience", "Experience"),
        ("general", "General")
    )

    trip = models.ForeignKey(TripModel, on_delete=models.CASCADE, related_name="NoteModel_trip")
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=EXCURSIONS)
    img = models.ImageField(upload_to='notes', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} in {self.trip.city}'
