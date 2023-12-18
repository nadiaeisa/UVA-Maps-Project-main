from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]

    place = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    justification = models.TextField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.place
    

class PlaceRating(models.Model):
    user = models.CharField(default="none", max_length=255)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.feedback.place} - {self.rating}"
