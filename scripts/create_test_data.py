import os
import sys
import django
# Ensure project root is on PYTHONPATH so Django settings package can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
try:
    django.setup()
except Exception as e:
    print('Error setting up Django:', e)
    raise
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

# Additional sample providers across categories
sample_providers = [
    {'name':'Raj Kumar','email':'raj.elec@example.com','phone':'+911111111111','profession':'Electrician','location':'Mumbai','city':'Mumbai','bio':'Expert electrician with 10+ years experience.','rating':4.8,'total_jobs':287,'verified':True,'experience_years':12},
    {'name':'Mohit Singh','email':'mohit.plumb@example.com','phone':'+911222222222','profession':'Plumber','location':'Mumbai','city':'Mumbai','bio':'Reliable plumber for homes and offices.','rating':4.5,'total_jobs':145,'verified':True,'experience_years':8},
    {'name':'Priya Sharma','email':'priya.clean@example.com','phone':'+911333333333','profession':'Cleaner','location':'Pune','city':'Pune','bio':'Professional cleaning services with attention to detail.','rating':4.9,'total_jobs':512,'verified':True,'experience_years':6},
    {'name':'Arun Patel','email':'arun.ac@example.com','phone':'+911444444444','profession':'AC Specialist','location':'Pune','city':'Pune','bio':'AC repair and maintenance specialist.','rating':4.7,'total_jobs':198,'verified':True,'experience_years':10},
    {'name':'Vikram Auto','email':'vikram.auto@example.com','phone':'+911555555555','profession':'Car Mechanic','location':'Mumbai','city':'Mumbai','bio':'Experienced car mechanic for quick service.','rating':4.4,'total_jobs':356,'verified':True,'experience_years':9},
]

for sp in sample_providers:
    prov, created = ServiceProvider.objects.get_or_create(email=sp['email'], defaults={
        'name': sp['name'],
        'phone': sp['phone'],
        'profession': sp['profession'],
        'location': sp['location'],
        'city': sp['city'],
        'address': f"{sp['city']} main street",
        'bio': sp['bio'],
        'avatar_url': '',
        'rating': sp.get('rating', 0.0),
        'total_jobs': sp.get('total_jobs', 0),
        'verified': sp.get('verified', False),
        'experience_years': sp.get('experience_years', 0),
    })
    if created:
        print('Created sample provider', prov.email)
    else:
        # update stats if needed
        prov.rating = sp.get('rating', prov.rating)
        prov.total_jobs = sp.get('total_jobs', prov.total_jobs)
        prov.verified = sp.get('verified', prov.verified)
        prov.experience_years = sp.get('experience_years', prov.experience_years)
        prov.save()
        print('Updated sample provider', prov.email)

print('Sample providers ready')
