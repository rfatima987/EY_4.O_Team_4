#!/usr/bin/env python
import os
import django
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from services.models import ServiceProvider, Booking

User = get_user_model()

# Clean up any previous test users/providers
User.objects.filter(username='prov_ui').delete()
User.objects.filter(username='cust_ui').delete()
ServiceProvider.objects.filter(email='prov_ui@example.com').delete()

# Create provider record without user
provider = ServiceProvider.objects.create(
    user=None,
    name='Provider UI Test',
    email='prov_ui@example.com',
    phone='9999999999',
    location='City',
    city='City',
    service_type='Test',
    profession='Test'
)
print('Created provider id', provider.id, 'availability', provider.availability)

# Create provider user with same email to auto-link
prov_user = User.objects.create_user(username='prov_ui', email='prov_ui@example.com', password='provpass')
print('Created provider user', prov_user.username)

# Use client to login as provider and POST to provider settings to set not_available
client = Client()
client.login(username='prov_ui', password='provpass')
resp = client.post('/provider/settings/', {'availability': 'not_available', 'action': 'update_availability'})
print('POST /provider/settings/ status', resp.status_code)
provider.refresh_from_db()
print('Provider availability after POST:', provider.availability)

# Now create a customer and attempt to book
cust = User.objects.create_user(username='cust_ui', email='cust_ui@example.com', password='custpass')
client.logout()
client.login(username='cust_ui', password='custpass')
# Try GET booking
get_resp = client.get(f'/booking/{provider.id}/')
print('GET booking status (should be redirect if unavailable):', get_resp.status_code)
# Try POST booking
post_data = {
    'customer_name': 'Customer UI',
    'customer_phone': '1112223333',
    'customer_address': '123 Test St',
    'service': 'Test Service',
    'booking_date': '2026-02-27',
    'booking_time': '10:00'
}
post_resp = client.post(f'/booking/{provider.id}/', post_data)
print('POST booking status:', post_resp.status_code, 'redirect:', getattr(post_resp, 'url', None))
print('Bookings count for provider:', Booking.objects.filter(provider=provider).count())

# Set provider available via settings and try booking again
client.logout()
client.login(username='prov_ui', password='provpass')
client.post('/provider/settings/', {'availability': 'available', 'action': 'update_availability'})
provider.refresh_from_db()
print('Provider availability after enabling:', provider.availability)
client.logout()
client.login(username='cust_ui', password='custpass')
post_resp2 = client.post(f'/booking/{provider.id}/', post_data, follow=True)
print('POST after available status:', post_resp2.status_code)
print('Bookings count after available:', Booking.objects.filter(provider=provider).count())

print('UI availability test finished.')

# Attempt duplicate booking on same date/time (should be blocked)
post_resp3 = client.post(f'/booking/{provider.id}/', post_data)
print('POST duplicate booking status (should be blocked):', post_resp3.status_code, 'redirect:', getattr(post_resp3, 'url', None))
print('Bookings count after duplicate attempt (should remain same):', Booking.objects.filter(provider=provider).count())
