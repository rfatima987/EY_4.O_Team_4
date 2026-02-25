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

# Authentication
auth_patterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]

# Main Dashboard (Role-based routing)
dashboard_patterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]

# Customer Routes
customer_patterns = [
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/find-services/', views.find_services, name='find_services'),
    path('customer/my-bookings/', views.my_bookings, name='my_bookings'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('customer/settings/', views.customer_settings, name='customer_settings'),
]

# Provider Routes
provider_patterns = [
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/my-requests/', views.provider_requests, name='provider_requests'),
    path('provider/my-services/', views.provider_services, name='provider_services'),
    path('provider/profile/', views.provider_profile, name='provider_profile'),
    path('provider/settings/', views.provider_settings, name='provider_settings'),
    path('provider/register/', views.add_provider, name='add_provider'),
]

# Service & Booking Operations
service_patterns = [
    path('providers/', views.providers, name='providers'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('booking/<int:provider_id>/', views.create_booking, name='booking_form'),
    path('booking/<int:booking_id>/update/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('bookings/status/', views.bookings_status, name='bookings_status'),
    path('api/bookings/', views.get_bookings_api, name='get_bookings_api'),
    path('api/provider-bookings/', views.get_provider_bookings_api, name='get_provider_bookings_api'),
]

# Legacy routes (backwards compatibility)
legacy_patterns = [
    path('profile/', views.user_profile, name='profile'),
    path('settings/', views.user_settings, name='settings'),
    path('register/', views.add_provider, name='add_provider_legacy'),
    path('provider-dashboard/', views.provider_dashboard, name='provider_dashboard_legacy'),
    path('my-bookings/', views.my_bookings, name='my_bookings_legacy'),
]

urlpatterns = auth_patterns + dashboard_patterns + customer_patterns + provider_patterns + service_patterns + legacy_patterns