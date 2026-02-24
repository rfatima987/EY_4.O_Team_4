"""
URL configuration for fixnear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.user_profile, name='profile'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('settings/', views.user_settings, name='settings'),
    path('providers/', views.providers, name='providers'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('register/', views.add_provider, name='add_provider'),
    path('booking/<int:provider_id>/', views.create_booking, name='booking_form'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('provider-dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('booking/<int:booking_id>/update/<str:status>/', views.update_booking_status, name='update_booking_status'),
]