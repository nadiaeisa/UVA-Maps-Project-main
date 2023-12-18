from django.contrib import admin
from .models import Feedback, PlaceRating


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'status', 'rating')  


@admin.register(PlaceRating)
class PlaceRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback', 'rating', 'timestamp')

    def feedback(self, obj):
        return obj.feedback.place  
