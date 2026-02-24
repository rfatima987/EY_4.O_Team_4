from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServiceProvider, Booking

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

@login_required(login_url='login')
def user_profile(request):
    """User profile page"""
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url='login')
def user_dashboard(request):
    """User dashboard page"""
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user_dashboard.html', context)

@login_required(login_url='login')
def user_settings(request):
    """User settings page"""
    user = request.user
    if request.method == 'POST':
        # Handle settings update
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    context = {
        'user': user,
    }
    return render(request, 'user_settings.html', context)

# ==================== BOOKING VIEWS ====================

@login_required(login_url='login')
def create_booking(request, provider_id):
    """Create a new booking for a provider"""
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email', '')
        customer_address = request.POST.get('customer_address')
        service = request.POST.get('service')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        notes = request.POST.get('notes', '')
        
        # Validate required fields
        if not all([customer_name, customer_phone, customer_address, service, booking_date, booking_time]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('booking_form', provider_id=provider_id)
        
        # Create booking
        booking = Booking.objects.create(
            provider=provider,
            customer_user=request.user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email or request.user.email,
            customer_address=customer_address,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            notes=notes,
            status='pending'
        )
        
        messages.success(request, f'Booking created successfully! Your booking ID is #{booking.id}. Status: Pending')
        return redirect('my_bookings')
    
    context = {
        'provider': provider,
        'user': request.user,
    }
    return render(request, 'booking_form.html', context)

@login_required(login_url='login')
def my_bookings(request):
    """View all bookings made by the customer"""
    bookings = Booking.objects.filter(customer_user=request.user).select_related('provider')
    
    context = {
        'bookings': bookings,
        'user': request.user,
    }
    return render(request, 'my_bookings.html', context)

@login_required(login_url='login')
def provider_dashboard(request):
    """Provider dashboard to manage bookings"""
    # Check if user is a provider
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        messages.error(request, 'You are not registered as a service provider. Please register first.')
        return redirect('add_provider')
    
    bookings = Booking.objects.filter(provider=provider).order_by('-created_at')
    
    # Statistics
    pending_count = bookings.filter(status='pending').count()
    approved_count = bookings.filter(status='approved').count()
    rejected_count = bookings.filter(status='rejected').count()
    
    context = {
        'provider': provider,
        'bookings': bookings,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'provider_dashboard.html', context)

@login_required(login_url='login')
def update_booking_status(request, booking_id, status):
    """Update booking status (approve/reject)"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is the provider
    try:
        provider = ServiceProvider.objects.get(user=request.user)
        if booking.provider != provider:
            messages.error(request, 'You do not have permission to update this booking.')
            return redirect('provider_dashboard')
    except ServiceProvider.DoesNotExist:
        messages.error(request, 'You are not a service provider.')
        return redirect('home')
    
    # Validate status
    valid_statuses = ['approved', 'rejected', 'completed', 'cancelled']
    if status not in valid_statuses:
        messages.error(request, 'Invalid status update.')
        return redirect('provider_dashboard')
    
    old_status = booking.status
    booking.status = status
    booking.save()
    
    # Update provider stats
    if status == 'approved' and old_status == 'pending':
        provider.total_jobs += 1
        provider.save()
    
    status_display = dict(booking.STATUS_CHOICES).get(status, status)
    messages.success(request, f'Booking #{booking.id} status updated to {status_display}.')
    return redirect('provider_dashboard')