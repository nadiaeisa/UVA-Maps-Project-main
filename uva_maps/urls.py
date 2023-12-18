from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "uva_maps"
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name='login'),
    path('user/', views.user, name='user'),
    path('admin/', views.admin, name='admin'),
    path("", views.logout_view, name = 'logout'),
    path('admin_approval/', views.admin_approval, name="admin_approval"),
    path('user_feedback/', views.user_feedback, name="user_feedback"),
    path('approve_feedback/<int:feedback_id>/', views.approve_feedback, name='approve_feedback'),
    path('reject_feedback/<int:feedback_id>/', views.reject_feedback, name='reject_feedback'),
    path('update_description', views.update_description, name='update_description'),
    path('submit_rating/<int:feedback_id>/', views.submit_rating, name='submit_rating'),
    path('get_updated_rating/<int:feedback_id>/', views.get_updated_rating, name='get_updated_rating')
]
