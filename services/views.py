from django.shortcuts import render, redirect, get_object_or_404
from .models import ServiceProvider

def home(request):
    """Home page with hero, services, how it works, and featured providers"""
    return render(request, 'index_new.html')

def providers(request):
    """List all service providers with filtering"""
    providers = ServiceProvider.objects.all()
    
    # Filter by service type if specified
    service_type = request.GET.get('service')
    if service_type:
        providers = providers.filter(profession__icontains=service_type)
    
    # Filter by location if specified
    location = request.GET.get('location')
    if location:
        providers = providers.filter(location__icontains=location)
    
    # Filter by rating if specified
    rating = request.GET.get('rating')
    if rating:
        providers = providers.filter(rating__gte=float(rating))
    
    context = {'providers': providers}
    return render(request, 'providers_list.html', context)

def provider_detail(request, provider_id):
    """Detailed view of a single provider"""
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    return render(request, 'provider_profile.html', {'provider': provider})

def add_provider(request):
    """Form for service providers to register"""
    if request.method == "POST":
        ServiceProvider.objects.create(
            name=request.POST.get('first_name', '') + ' ' + request.POST.get('last_name', ''),
            profession=request.POST.get('service_type', ''),
            phone=request.POST.get('phone', ''),
            location=request.POST.get('city', ''),
            email=request.POST.get('email', '')
        )
        return redirect('providers')
    return render(request, 'provider_registration.html')