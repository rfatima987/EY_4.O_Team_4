import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
django.setup()
from django.contrib.auth.models import User
from services.models import ServiceProvider, Booking
from django.utils import timezone
from datetime import date, time

# Create provider user
p_email = 'test_provider@example.com'
provider_user, created = User.objects.get_or_create(username='test_provider', defaults={'email': p_email, 'first_name':'Test','last_name':'Provider'})
if created:
    provider_user.set_password('password123')
    provider_user.save()
    print('Created provider user', provider_user.email)
else:
    print('Provider user exists', provider_user.email)

# Create customer user
c_email = 'test_customer@example.com'
customer_user, created = User.objects.get_or_create(username='test_customer', defaults={'email': c_email, 'first_name':'Test','last_name':'Customer'})
if created:
    customer_user.set_password('password123')
    customer_user.save()
    print('Created customer user', customer_user.email)
else:
    print('Customer user exists', customer_user.email)

# Create ServiceProvider profile (link to provider_user)
provider_profile, created = ServiceProvider.objects.get_or_create(email=p_email, defaults={
    'name':'Test Provider',
    'phone':'+911234567890',
    'profession':'General',
    'location':'Test City',
    'city':'Test City',
    'address':'123 Test St',
    'bio':'Test provider bio',
    'avatar_url':'',
})
if created:
    provider_profile.user = provider_user
    provider_profile.save()
    print('Created provider profile and linked to user')
else:
    if provider_profile.user is None:
        provider_profile.user = provider_user
        provider_profile.save()
        print('Linked existing provider profile to user')
    else:
        print('Provider profile exists and linked')

# Create a booking by customer for provider
booking = Booking.objects.create(
    provider=provider_profile,
    customer_user=customer_user,
    customer_name=f'{customer_user.first_name} {customer_user.last_name}',
    customer_phone='+919999999999',
    customer_email=customer_user.email,
    customer_address='42 Example Lane, Test City',
    service='Test Service',
    booking_date=date.today(),
    booking_time=time(hour=10, minute=30),
    notes='This is a test booking',
    status='pending'
)
print('Created booking id', booking.id)
print('Done')
