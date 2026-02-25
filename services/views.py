from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServiceProvider, Booking
from django.http import JsonResponse
import os
from django.core.files.storage import default_storage
from django.db.models import Q
from django.db.models import Avg
from .models import Review

@login_required(login_url='login')
def submit_review(request):
    """Submit a review tied to a completed booking.

    POST params expected: booking_id, provider_id, rating, comment
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    booking_id = request.POST.get('booking_id')
    provider_id = request.POST.get('provider_id')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '').strip()

    # Basic validation
    try:
        booking = Booking.objects.select_related('provider', 'customer_user').get(id=int(booking_id))
    except Exception:
        return JsonResponse({'error': 'Booking not found'}, status=404)

    if booking.customer_user != request.user:
        return JsonResponse({'error': 'You are not the owner of this booking'}, status=403)

    if booking.status != 'completed':
        return JsonResponse({'error': 'Cannot review a booking that is not completed'}, status=400)

    # Prevent duplicate review for same booking
    if hasattr(booking, 'review'):
        return JsonResponse({'error': 'A review for this booking already exists'}, status=400)

    try:
        provider = ServiceProvider.objects.get(id=int(provider_id))
    except Exception:
        return JsonResponse({'error': 'Provider not found'}, status=404)

    try:
        rating_val = int(rating)
        if rating_val < 1 or rating_val > 5:
            raise ValueError()
    except Exception:
        return JsonResponse({'error': 'Invalid rating value'}, status=400)

    # Create review
    review = Review.objects.create(
        booking=booking,
        provider=provider,
        user=request.user,
        rating=rating_val,
        comment=comment
    )

    # Provider.rating is maintained in Review.save(); return success
    return JsonResponse({'success': True, 'new_rating': provider.rating})

# ==================== VALIDATION HELPERS ====================

def validate_certificate_file(file_obj):
    """Validate uploaded certificate file. Returns (is_valid, error_msg)."""
    if not file_obj:
        return True, None  # Optional file
    
    ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/png']
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    
    if file_obj.content_type not in ALLOWED_TYPES:
        return False, 'Certificate must be PDF, JPG or PNG format'
    
    if file_obj.size > MAX_SIZE:
        return False, f'Certificate file must be ≤ 5MB (yours is {file_obj.size / 1024 / 1024:.1f}MB)'
    
    return True, None

def validate_aadhar(aadhar_str):
    """Validate Aadhar/ID number. Returns (is_valid, error_msg)."""
    if not aadhar_str:
        return True, None  # Optional field
    
    cleaned = ''.join(c for c in str(aadhar_str) if c.isalnum())
    if len(cleaned) < 6:
        return False, 'Aadhar/ID must be at least 6 characters'
    
    if len(cleaned) > 64:
        return False, 'Aadhar/ID is too long'
    
    return True, None

def delete_old_certificate(provider):
    """Safely delete old certificate file if it exists."""
    if provider.certificate:
        try:
            if default_storage.exists(provider.certificate.name):
                default_storage.delete(provider.certificate.name)
        except Exception:
            pass  # Silently fail if deletion doesn't work

# Helper function to check if user is a provider
def get_user_provider(user):
    """Get provider for user or None if not a provider. Auto-links by email."""
    if not user.is_authenticated:
        return None
    try:
        return ServiceProvider.objects.get(user=user)
    except ServiceProvider.DoesNotExist:
        # Try to auto-link by email
        if user.email:
            matches = ServiceProvider.objects.filter(email__iexact=user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = user
                provider.save()
                return provider
        return None

# Helper function to add provider context to response
def add_provider_context(context, user):
    """Add 'is_provider' and 'provider' to context for role-based templates."""
    provider = get_user_provider(user) if user.is_authenticated else None
    context['is_provider'] = provider is not None
    context['provider'] = provider
    return context

def home(request):
    """Home page with hero, services, how it works, and featured providers"""
    # Load featured providers (top-rated). If none verified, fall back to any providers.
    featured = ServiceProvider.objects.filter(verified=True).order_by('-rating', '-total_jobs')[:6]
    if not featured.exists():
        featured = ServiceProvider.objects.all().order_by('-rating', '-total_jobs')[:6]

    context = {'featured_providers': featured}
    return render(request, 'index.html', add_provider_context(context, request.user))

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
                city=city,
                profession='General',
                experience_years=0
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

    # Filter by service type if specified (support flexible matching)
    service_type = (request.GET.get('service') or '').strip()
    if service_type:
        term = service_type.lower()
        # Build simple variants to match common suffix differences (electrical vs electrician, etc.)
        variants = {term}
        if term.endswith('ical'):
            variants.add(term.replace('ical', 'ician'))
        if term.endswith('ician'):
            variants.add(term.replace('ician', 'ical'))
        # Also add a short root to help partial matches
        root = ''.join(ch for ch in term if ch.isalpha())
        if len(root) > 3:
            variants.add(root[:5])

        q = Q()
        for v in variants:
            q |= Q(profession__icontains=v)
            q |= Q(service_type__icontains=v)
            q |= Q(name__icontains=v)
            q |= Q(bio__icontains=v)

        providers = providers.filter(q)

    # Filter by profession if specified (case-insensitive match across profession/service_type/name/bio)
    profession_q = (request.GET.get('profession') or '').strip()
    if profession_q:
        pq = Q()
        pq |= Q(profession__icontains=profession_q)
        pq |= Q(service_type__icontains=profession_q)
        pq |= Q(name__icontains=profession_q)
        pq |= Q(bio__icontains=profession_q)
        providers = providers.filter(pq)

    # Filter by location if specified (check multiple location fields)
    location = (request.GET.get('location') or '').strip()
    if location:
        providers = providers.filter(
            Q(location__icontains=location) | Q(city__icontains=location) | Q(state__icontains=location)
        )

    # Filter by rating if specified
    rating = request.GET.get('rating')
    if rating:
        try:
            providers = providers.filter(rating__gte=float(rating))
        except (ValueError, TypeError):
            pass

    context = {'providers': providers}
    return render(request, 'providers_list.html', context)

def provider_detail(request, provider_id):
    """Detailed view of a single provider"""
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    return render(request, 'provider_profile.html', {'provider': provider})


def provider_reviews_api(request, provider_id):
    """Return paginated reviews for a provider as JSON.

    Query params: page (1-based), per_page
    """
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
    except ServiceProvider.DoesNotExist:
        return JsonResponse({'error': 'Provider not found'}, status=404)

    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    all_reviews = provider.reviews.order_by('-created_at')
    total = all_reviews.count()
    start = (page - 1) * per_page
    end = start + per_page
    reviews_qs = all_reviews[start:end]

    reviews = []
    for r in reviews_qs:
        reviews.append({
            'id': r.id,
            'user': r.user.get_full_name() or r.user.username,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d')
        })

    return JsonResponse({'total': total, 'page': page, 'per_page': per_page, 'reviews': reviews})

@login_required(login_url='login')
def add_provider(request):
    """Form for service providers to register"""
    # If user already has a provider profile, redirect them
    existing = ServiceProvider.objects.filter(user=request.user).first()
    if existing:
        messages.info(request, 'You already have a provider profile.')
        return redirect('provider_dashboard')

    if request.method == "POST":
        # Collect fields from form
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', request.user.email or '').strip()
        phone = request.POST.get('phone', '').strip()
        service_type = request.POST.get('service_type', '')
        profession = request.POST.get('profession', '').strip() or service_type
        experience = request.POST.get('experience', 0)
        bio = request.POST.get('bio', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        address = request.POST.get('address', '')
        hourly_rate = request.POST.get('hourly_rate', 0)
        call_charge = request.POST.get('call_charge', 0)
        availability = request.POST.get('availability', 'available')
        aadhar = request.POST.get('aadhar', '').strip()
        cert_file = request.FILES.get('certificate')

        # Server-side validation
        # Basic required fields (profession required per new rules)
        if not (first_name and last_name and email and phone and city and profession):
            messages.error(request, 'Please fill in all required fields and provide your profession.')
            return render(request, 'provider_registration.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'city': city,
                'state': state,
                'profession': profession,
                'experience': experience,
            })

        # Validate certificate file
        cert_valid, cert_error = validate_certificate_file(cert_file)
        if not cert_valid:
            messages.error(request, cert_error)
            return render(request, 'provider_registration.html')

        # Validate aadhar
        aadhar_valid, aadhar_error = validate_aadhar(aadhar)
        if not aadhar_valid:
            messages.error(request, aadhar_error)
            return render(request, 'provider_registration.html')

        # Validate profession (non-empty)
        if not profession:
            messages.error(request, 'Profession cannot be empty.')
            return render(request, 'provider_registration.html', {'profession': profession, 'experience': experience})

        # Validate experience - must be integer and non-negative
        try:
            exp_int = int(experience or 0)
            if exp_int < 0:
                raise ValueError()
        except Exception:
            messages.error(request, 'Experience must be a valid non-negative integer representing years.')
            return render(request, 'provider_registration.html', {'profession': profession, 'experience': experience})

        # Prevent duplicate provider for same user/email
        existing_by_email = ServiceProvider.objects.filter(email__iexact=email).first()
        if existing_by_email and existing_by_email.user and existing_by_email.user != request.user:
            messages.error(request, 'A provider account already exists with this email.')
            return render(request, 'provider_registration.html')

        # If a provider exists with this email but not linked to a user, link it
        if existing_by_email and not existing_by_email.user:
            provider = existing_by_email
            provider.user = request.user
            provider.name = f"{first_name} {last_name}"
            provider.profession = profession
            provider.phone = phone
            provider.location = city
            provider.city = city
            provider.state = state
            provider.address = address
            provider.experience_years = exp_int
            try:
                provider.hourly_rate = float(hourly_rate or 0)
                provider.call_charge = float(call_charge or 0)
            except Exception:
                pass
            provider.bio = bio
            provider.availability = availability or provider.availability
            provider.aadhar_number = aadhar
            
            # Handle certificate: delete old, add new
            if cert_file:
                delete_old_certificate(provider)
                provider.certificate = cert_file
            
            provider.save()
            messages.success(request, 'Provider profile linked to your account successfully!')
            return redirect('provider_dashboard')

        # Create new provider and link to current user
        provider = ServiceProvider.objects.create(
            user=request.user,
            name=f"{first_name} {last_name}",
            profession=profession,
            phone=phone,
            location=city,
            city=city,
            state=state,
            address=address,
            email=email,
            experience_years=exp_int,
            hourly_rate=hourly_rate or 0,
            call_charge=call_charge or 0,
            bio=bio,
            availability=('available' if availability in ['24/7','available','weekdays','weekends','custom'] else 'available'),
            aadhar_number=aadhar
        )
        
        # Attach certificate if provided
        if cert_file:
            provider.certificate = cert_file
            provider.save()

        messages.success(request, 'Provider profile created and linked to your account successfully!')
        return redirect('provider_dashboard')

    # GET - render form prefilled with user info where available
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': '',
        'city': '',
        'service_type': '',
        'profession': '',
        'experience': 0,
        'bio': '',
        'state': '',
        'address': '',
        'hourly_rate': '',
        'call_charge': '',
        'availability': 'available',
        'aadhar': '',
    }
    return render(request, 'provider_registration.html', context)

@login_required(login_url='login')
def user_profile(request):
    """User profile page"""
    user = request.user
    context = {
        'user': user,
    }
    # Add provider context so provider fields can be shown on the profile
    return render(request, 'user_profile.html', add_provider_context(context, request.user))

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
        # Also update provider fields if this user is a provider
        provider = get_user_provider(request.user)
        if provider:
            profession = request.POST.get('profession', '').strip()
            experience = request.POST.get('experience_years', None)
            if profession:
                provider.profession = profession
            try:
                if experience is not None and str(experience).strip() != '':
                    exp_val = int(experience)
                    if exp_val >= 0:
                        provider.experience_years = exp_val
            except Exception:
                messages.warning(request, 'Experience must be a non-negative integer. Value ignored.')
            provider.save()

        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    context = {
        'user': user,
    }
    return render(request, 'user_settings.html', add_provider_context(context, request.user))

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
        'force_customer_nav': True,  # Force customer navigation, hide provider nav
    }
    return render(request, 'my_bookings.html', context)

@login_required(login_url='login')
def provider_dashboard(request):
    """Provider dashboard to manage bookings"""
    # Resolve provider record linked to this user. If an existing provider profile
    # was created earlier without linking to the user, try to auto-link by email.
    provider = None
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        # Try to find a provider profile with the same email and link it
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
        if not provider:
            messages.error(request, 'You are not registered as a service provider. Please register first.')
            return redirect('add_provider')
    
    # Filter bookings based on status filter if provided
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.filter(provider=provider).order_by('-created_at')
    
    if status_filter and status_filter in ['pending', 'approved', 'rejected', 'completed', 'cancelled']:
        bookings = bookings.filter(status=status_filter)
    
    # Statistics
    all_bookings = Booking.objects.filter(provider=provider)
    pending_count = all_bookings.filter(status='pending').count()
    approved_count = all_bookings.filter(status='approved').count()
    rejected_count = all_bookings.filter(status='rejected').count()
    completed_count = all_bookings.filter(status='completed').count()
    cancelled_count = all_bookings.filter(status='cancelled').count()
    
    # Calculate completion rate
    total_bookings = all_bookings.count()
    completion_rate = (completed_count / total_bookings * 100) if total_bookings > 0 else 0
    
    context = {
        'provider': provider,
        'bookings': bookings,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'total_bookings': total_bookings,
        'completion_rate': round(completion_rate, 1),
        'status_filter': status_filter,
    }
    return render(request, 'provider_dashboard.html', context)

@login_required(login_url='login')
def update_booking_status(request, booking_id, status):
    """Update booking status (approve/reject)"""
    # Only allow POST requests for status updates
    if request.method != 'POST':
        messages.error(request, 'Invalid request method for updating booking status.')
        return redirect('provider_dashboard')

    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is the provider
    provider = None
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        # Attempt to auto-link by email if possible
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
    if not provider:
        messages.error(request, 'You are not a service provider.')
        return redirect('home')
    if booking.provider != provider:
        messages.error(request, 'You do not have permission to update this booking.')
        return redirect('provider_dashboard')
    
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


@login_required(login_url='login')
def bookings_status(request):
    """Return JSON statuses for current user's bookings (customer view)."""
    bookings = Booking.objects.filter(customer_user=request.user).values('id', 'status')
    data = {b['id']: b['status'] for b in bookings}
    return JsonResponse({'bookings': data})


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    """Cancel a booking (customer can only cancel pending bookings)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is the customer
    if booking.customer_user != request.user:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('my_bookings')
    
    # Can only cancel pending or approved bookings
    if booking.status not in ['pending', 'approved']:
        messages.error(request, f'Cannot cancel a {booking.status} booking.')
        return redirect('my_bookings')
    
    booking.status = 'cancelled'
    booking.save()
    
    messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
    return redirect('my_bookings')


@login_required(login_url='login')
def get_bookings_api(request):
    """Advanced bookings API with filtering and pagination"""
    user = request.user
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    provider_id = request.GET.get('provider', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', '-created_at')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    # Base query for customer bookings
    bookings = Booking.objects.filter(customer_user=user)
    
    # Apply filters
    if status_filter and status_filter in ['pending', 'approved', 'rejected', 'completed', 'cancelled']:
        bookings = bookings.filter(status=status_filter)
    
    if provider_id:
        try:
            bookings = bookings.filter(provider_id=int(provider_id))
        except (ValueError, TypeError):
            pass
    
    if date_from:
        try:
            from datetime import datetime
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            bookings = bookings.filter(booking_date__gte=df)
        except (ValueError, TypeError):
            pass
    
    if date_to:
        try:
            from datetime import datetime
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            bookings = bookings.filter(booking_date__lte=dt)
        except (ValueError, TypeError):
            pass
    
    # Sort
    if sort_by in ['-created_at', 'created_at', '-booking_date', 'booking_date', '-updated_at', 'updated_at']:
        bookings = bookings.order_by(sort_by)
    
    # Pagination
    total_count = bookings.count()
    start = (page - 1) * per_page
    end = start + per_page
    paginated_bookings = bookings[start:end]
    
    # Build response
    data = {
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_count + per_page - 1) // per_page,
        'bookings': [
            {
                'id': b.id,
                'provider_name': b.provider.name,
                'provider_id': b.provider.id,
                'service': b.service,
                'date': str(b.booking_date),
                'time': str(b.booking_time),
                'status': b.status,
                'created_at': b.created_at.isoformat(),
                'updated_at': b.updated_at.isoformat(),
            }
            for b in paginated_bookings
        ]
    }
    
    return JsonResponse(data)


@login_required(login_url='login')
def get_provider_bookings_api(request):
    """API endpoint for provider to get their bookings with analytics"""
    # Get provider
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
            else:
                return JsonResponse({'error': 'Not a service provider'}, status=403)
        else:
            return JsonResponse({'error': 'Not a service provider'}, status=403)
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    # Get bookings
    bookings = Booking.objects.filter(provider=provider)
    
    # Apply filters
    if status_filter and status_filter in ['pending', 'approved', 'rejected', 'completed', 'cancelled']:
        bookings = bookings.filter(status=status_filter)
    
    if date_from:
        try:
            from datetime import datetime
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            bookings = bookings.filter(booking_date__gte=df)
        except (ValueError, TypeError):
            pass
    
    if date_to:
        try:
            from datetime import datetime
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            bookings = bookings.filter(booking_date__lte=dt)
        except (ValueError, TypeError):
            pass
    
    bookings = bookings.order_by('-created_at')
    
    # Calculate statistics
    all_bookings = Booking.objects.filter(provider=provider)
    total = all_bookings.count()
    pending = all_bookings.filter(status='pending').count()
    approved = all_bookings.filter(status='approved').count()
    completed = all_bookings.filter(status='completed').count()
    rejected = all_bookings.filter(status='rejected').count()
    cancelled = all_bookings.filter(status='cancelled').count()
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Pagination
    total_count = bookings.count()
    start = (page - 1) * per_page
    end = start + per_page
    paginated_bookings = bookings[start:end]
    
    # Build response
    data = {
        'provider': {
            'id': provider.id,
            'name': provider.name,
            'profession': provider.profession,
            'rating': float(provider.rating),
        },
        'stats': {
            'total': total,
            'pending': pending,
            'approved': approved,
            'completed': completed,
            'rejected': rejected,
            'cancelled': cancelled,
            'completion_rate': round(completion_rate, 1),
        },
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total_count,
            'total_pages': (total_count + per_page - 1) // per_page,
        },
        'bookings': [
            {
                'id': b.id,
                'customer_name': b.customer_name,
                'customer_phone': b.customer_phone,
                'service': b.service,
                'date': str(b.booking_date),
                'time': str(b.booking_time),
                'address': b.customer_address,
                'notes': b.notes,
                'status': b.status,
                'created_at': b.created_at.isoformat(),
                'updated_at': b.updated_at.isoformat(),
            }
            for b in paginated_bookings
        ]
    }
    
    return JsonResponse(data)


# ==================== ROLE-BASED DASHBOARD ROUTING ====================

@login_required(login_url='login')
def dashboard(request):
    """Smart dashboard that routes to customer or provider dashboard based on role"""
    # Check if user is a provider
    try:
        provider = ServiceProvider.objects.get(user=request.user)
        return redirect('provider_dashboard')
    except ServiceProvider.DoesNotExist:
        # Check if email matches an existing provider profile
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                return redirect('provider_dashboard')
        # User is a customer
        return redirect('customer_dashboard')


# ==================== CUSTOMER VIEWS ====================

@login_required(login_url='login')
def customer_dashboard(request):
    """Customer dashboard - overview of recent bookings and quick actions"""
    user = request.user
    recent_bookings = Booking.objects.filter(customer_user=user).order_by('-created_at')[:5]
    
    # Get comprehensive statistics
    all_bookings = Booking.objects.filter(customer_user=user)
    total_bookings = all_bookings.count()
    completed_bookings = all_bookings.filter(status='completed').count()
    pending_bookings = all_bookings.filter(status='pending').count()
    approved_bookings = all_bookings.filter(status='approved').count()
    rejected_bookings = all_bookings.filter(status='rejected').count()
    cancelled_bookings = all_bookings.filter(status='cancelled').count()
    
    # Calculate success rate
    success_rate = (completed_bookings / total_bookings * 100) if total_bookings > 0 else 0
    
    context = {
        'user': user,
        'recent_bookings': recent_bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'approved_bookings': approved_bookings,
        'pending_bookings': pending_bookings,
        'rejected_bookings': rejected_bookings,
        'cancelled_bookings': cancelled_bookings,
        'success_rate': round(success_rate, 1),
        'force_customer_nav': True,  # Force customer navigation, hide provider nav
    }
    return render(request, 'customer_dashboard.html', context)


@login_required(login_url='login')
def find_services(request):
    """Customer page to find and search for service providers"""
    providers = ServiceProvider.objects.all()
    
    # Search filters
    search_query = request.GET.get('q', '')
    if search_query:
        providers = providers.filter(
            profession__icontains=search_query
        ) | providers.filter(
            bio__icontains=search_query
        )
    
    # Filter by profession
    profession = request.GET.get('profession', '')
    if profession:
        providers = providers.filter(profession__icontains=profession)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        providers = providers.filter(city__icontains=location)
    
    # Filter by rating
    min_rating = request.GET.get('rating', '')
    if min_rating:
        try:
            providers = providers.filter(rating__gte=float(min_rating))
        except (ValueError, TypeError):
            pass
    
    # Sort
    sort_by = request.GET.get('sort', '-rating')
    if sort_by in ['-rating', 'experience_years', 'hourly_rate']:
        providers = providers.order_by(sort_by)
    
    context = {
        'providers': providers,
        'search_query': search_query,
        'selected_profession': profession,
        'selected_location': location,
        'force_customer_nav': True,  # Force customer navigation, hide provider nav
    }
    return render(request, 'find_services.html', add_provider_context(context, request.user))


@login_required(login_url='login')
def customer_profile(request):
    """Customer profile page - view and edit personal information"""
    user = request.user
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('customer_profile')
    
    # Get booking stats
    total_bookings = Booking.objects.filter(customer_user=user).count()
    completed_bookings = Booking.objects.filter(customer_user=user, status='completed').count()
    
    context = {
        'user': user,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'force_customer_nav': True,  # Force customer navigation, hide provider nav
    }
    return render(request, 'customer_profile.html', context)


@login_required(login_url='login')
def customer_settings(request):
    """Customer settings page - preferences and account settings"""
    user = request.user
    
    if request.method == 'POST':
        # Handle settings update
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        # Update password if provided
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if old_password and new_password and confirm_password:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Password changed successfully!')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')
        
        user.save()
        if not (old_password and new_password):
            messages.success(request, 'Settings updated successfully!')
        return redirect('customer_settings')
    
    context = {
        'user': user,
        'force_customer_nav': True,  # Force customer navigation, hide provider nav
    }
    return render(request, 'customer_settings.html', context)


# ==================== PROVIDER VIEWS ====================

@login_required(login_url='login')
def provider_requests(request):
    """Provider page - view all incoming booking requests"""
    # Get or auto-link provider
    provider = get_user_provider(request.user)
    if not provider:
        messages.error(request, 'Please register as a service provider first.')
        return redirect('add_provider')
    
    # Get all pending bookings for this provider
    pending_requests = Booking.objects.filter(provider=provider, status='pending').order_by('-created_at')
    
    context = {
        'provider': provider,
        'requests': pending_requests,
    }
    return render(request, 'provider_requests.html', add_provider_context(context, request.user))


@login_required(login_url='login')
def provider_services(request):
    """Provider page - manage services offered"""
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
        if not provider:
            messages.error(request, 'Please register as a service provider first.')
            return redirect('add_provider')
    
    if request.method == 'POST':
        # Update service information
        provider.service_type = request.POST.get('service_type', provider.service_type)
        provider.profession = request.POST.get('profession', provider.profession)
        provider.hourly_rate = request.POST.get('hourly_rate', provider.hourly_rate)
        provider.call_charge = request.POST.get('call_charge', provider.call_charge)
        provider.bio = request.POST.get('bio', provider.bio)
        provider.save()
        messages.success(request, 'Services updated successfully!')
        return redirect('provider_services')
    
    context = {'provider': provider}
    return render(request, 'provider_services.html', context)


@login_required(login_url='login')
def provider_profile(request):
    """Provider profile page - view and edit professional information"""
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
        if not provider:
            messages.error(request, 'Please register as a service provider first.')
            return redirect('add_provider')
    
    if request.method == 'POST':
        # Update provider profile
        provider.name = request.POST.get('name', provider.name)
        provider.profession = request.POST.get('profession', provider.profession)
        # Validate experience_years input
        try:
            exp_val = int(request.POST.get('experience_years', provider.experience_years))
            if exp_val < 0:
                raise ValueError()
        except Exception:
            messages.error(request, 'Experience must be a non-negative integer.')
            return redirect('provider_profile')
        provider.experience_years = exp_val
        provider.phone = request.POST.get('phone', provider.phone)
        provider.address = request.POST.get('address', provider.address)
        provider.city = request.POST.get('city', provider.city)
        provider.bio = request.POST.get('bio', provider.bio)
        provider.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('provider_profile')
    
    # Get provider stats
    total_bookings = Booking.objects.filter(provider=provider).count()
    completed_bookings = Booking.objects.filter(provider=provider, status='completed').count()
    
    context = {
        'provider': provider,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
    }
    return render(request, 'provider_profile.html', context)


@login_required(login_url='login')
def provider_settings(request):
    """Provider settings page - manage account and notification settings"""
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        if request.user.email:
            matches = ServiceProvider.objects.filter(email__iexact=request.user.email)
            if matches.exists():
                provider = matches.first()
                provider.user = request.user
                provider.save()
        if not provider:
            messages.error(request, 'Please register as a service provider first.')
            return redirect('add_provider')
    
    if request.method == 'POST':
        # Update availability
        provider.availability = request.POST.get('availability', provider.availability)
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()
        
        provider.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('provider_settings')
    
    context = {
        'provider': provider,
        'user': request.user,
    }
    return render(request, 'provider_settings.html', context)