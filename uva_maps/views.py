from django.db.models import Avg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.conf import settings
from django.contrib import messages
from .mixins import Directions
from .models import Feedback
from .forms import FeedbackForm
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils import timezone
from .models import Feedback, PlaceRating
from datetime import timedelta
from django.http import JsonResponse

def submit_rating(request, feedback_id):
    if request.method == 'POST':
        user = request.user
        feedback = get_object_or_404(Feedback, pk=feedback_id)
        rating_value = request.POST.get('rating')
        existing_rating = PlaceRating.objects.filter(feedback=feedback, user=user)
        if existing_rating.exists():
            existing_rating.delete()
        PlaceRating.objects.create(feedback=feedback, rating=rating_value, user=user)
        new_average = calculate_average_rating(feedback_id)
        return JsonResponse({'newAverage': new_average})

def get_updated_rating(request, feedback_id):
    try:
        feedback = get_object_or_404(Feedback, pk=feedback_id)
        updated_rating = feedback.rating
        print(updated_rating)
        return JsonResponse({'updatedRating': updated_rating})
    except Feedback.DoesNotExist:
        return JsonResponse({'error': 'Feedback not found'}, status=404)

def calculate_average_rating(feedback_id):
    one_hour_ago = timezone.now() - timedelta(hours=1)
    ratings = PlaceRating.objects.filter(feedback_id=feedback_id, timestamp__gte=one_hour_ago)
    feedback = Feedback.objects.get(pk=feedback_id)
    if ratings.exists():
        average = ratings.aggregate(Avg('rating'))['rating__avg']
        feedback.rating = round(average, 1)
    else:
        feedback.rating = 0
    feedback.save() 
    return feedback.rating

def approve_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    feedback.status = Feedback.APPROVED
    feedback.save()
    return redirect('/uva_maps/admin_approval')

def reject_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    feedback.status = Feedback.REJECTED
    feedback.delete()
    return redirect('/uva_maps/admin_approval')

def user_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted successfully!')
            #feedback_submitted = True
            return redirect('/uva_maps/user_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/user_feedback.html', {'form': form})

@staff_member_required
def admin_approval(request):
    feedback_entries = Feedback.objects.all()
    feedback_entries = Feedback.objects.order_by('-status')
    return render(request, 'feedback/admin_approval.html', {'feedback_entries': feedback_entries})

@staff_member_required
def update_description(request):
    if request.method == 'POST':
        feedback_object = Feedback.objects.get(pk=request.POST.get("pk"))
        feedback_object.description = request.POST.get("newDescription")
        feedback_object.save()
    return redirect('/uva_maps/admin_approval')

def route(request):
    if not request.user.is_authenticated:
        return redirect('/uva_maps/user')
    approved_feedback = Feedback.objects.filter(status=Feedback.APPROVED)
    approved_feedback_data = [
        {'address': entry.address, 'place': entry.place, 'id': entry.id, 'description': entry.description,
         'rating': entry.rating} for entry in
        approved_feedback]
    context = {"google_api_key": settings.GOOGLE_API_KEY,
               "approved_feedback": json.dumps(approved_feedback_data)}
    return render(request, 'map/route.html', context)

def map(request):
    if not request.user.is_authenticated:
        return redirect('/uva_maps/user')
    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")
    directions = Directions(
        lat_a=lat_a,
        long_a=long_a,
        lat_b=lat_b,
        long_b=long_b
    )
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}',
        "directions": directions,
    }
    return render(request, 'map/map.html', context)

def index(request):
    if request.user.is_authenticated:
        return redirect('/uva_maps/user')
    return redirect('/uva_maps/login')

def login(request):
    if request.user.is_authenticated:
        return redirect('/uva_maps/user')
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect("/uva_maps/login")

@login_required
def user(request):
    return render(request, 'login/user.html')

@staff_member_required
def admin(request):
    return render(request, 'login/admin.html')
