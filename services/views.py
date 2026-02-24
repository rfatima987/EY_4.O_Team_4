from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServiceProvider

def home(request):
    """Home page with hero, services, how it works, and featured providers"""
    return render(request, 'index.html')

def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user_auth = authenticate(request, username=user.username, password=password)
            
            if user_auth is not None:
                login(request, user_auth)
                messages.success(request, f'Welcome back, {user_auth.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email. Please sign up.')
    
    return render(request, 'auth_login.html')

def signup_view(request):
    """User signup/registration page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        account_type = request.POST.get('account_type', 'customer')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'auth_signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return render(request, 'auth_signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login instead.')
            return render(request, 'auth_signup.html')
        
        # Create user account
        username = email.split('@')[0]  # Use email prefix as username
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # If signing up as provider, create provider profile
        if account_type == 'provider':
            ServiceProvider.objects.create(
                name=f'{first_name} {last_name}',
                email=email,
                phone=phone,
                location=city,
                city=city
            )
        
        # Auto-login the user
        login(request, user)
        messages.success(request, f'Welcome to FixNear, {first_name}!')
        
        if account_type == 'provider':
            return redirect('add_provider')
        return redirect('home')
    
    return render(request, 'auth_signup.html')

def logout_view(request):
    """Log out user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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

@login_required(login_url='login')
def add_provider(request):
    """Form for service providers to register"""
    if request.method == "POST":
        ServiceProvider.objects.create(
            name=request.POST.get('first_name', '') + ' ' + request.POST.get('last_name', ''),
            profession=request.POST.get('service_type', ''),
            phone=request.POST.get('phone', ''),
            location=request.POST.get('city', ''),
            email=request.POST.get('email', ''),
            experience_years=int(request.POST.get('experience_years', 0)),
            hourly_rate=float(request.POST.get('hourly_rate', 0)),
            bio=request.POST.get('bio', '')
        )
        messages.success(request, 'Provider profile created successfully!')
        return redirect('providers')
    return render(request, 'provider_registration.html')