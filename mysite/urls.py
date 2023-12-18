"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django.views.generic import RedirectView
from uva_maps import views

urlpatterns = [
    path('', RedirectView.as_view(url='uva_maps/login/'), name='index_redirect'),
    path('uva_maps/', include('uva_maps.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('route/', views.route, name="route"),
    path('map/', views.map, name="map"),
    path('admin_approval', views.admin_approval, name="admin_approval"),
    path('user_feedback', views.user_feedback, name="user_feedback"),
]
