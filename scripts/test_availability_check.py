#!/usr/bin/env python
import os
import django
import sys
import datetime

# Ensure project root is on sys.path so Django can import the project package
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from services.models import ServiceProvider, Booking

User = get_user_model()

try:
    # Create a test user (clean up previous if exists)
    User.objects.filter(username='tester_av').delete()
    user = User.objects.create_user(username='tester_av', email='tester_av@example.com', password='pass')

    # Create a provider
    ServiceProvider.objects.filter(name='Test Provider Auto').delete()
    provider = ServiceProvider.objects.create(
        user=None,
        name='Test Provider Auto',
        email='provider_auto@example.com',
        phone='0000000000',
        location='TestCity',
        city='TestCity',
        service_type='Test',
        profession='Test'
    )

    print('Provider created id=', provider.id, 'initial availability=', provider.availability)

    # Set provider unavailable
    provider.availability = 'not_available'
    provider.save()
    print('Provider availability set to', provider.availability)

    client = Client()
    logged_in = client.login(username='tester_av', password='pass')
    print('Client login ok?', logged_in)

    # Try to GET booking page
    get_resp = client.get(f'/booking/{provider.id}/')
    print('GET /booking/ status_code=', get_resp.status_code)

    # Try to POST booking
    post_data = {
        'customer_name': 'Alice',
        'customer_phone': '1112223333',
        'customer_address': '123 Test St',
        'service': 'Test Service',
        'booking_date': str(datetime.date.today()),
        'booking_time': '10:00'
    }
    post_resp = client.post(f'/booking/{provider.id}/', post_data)
    print('POST /booking/ status_code=', post_resp.status_code, 'redirect:', getattr(post_resp, 'url', None))

    # Verify no booking created
    count_after = Booking.objects.filter(provider=provider).count()
    print('Bookings for provider after attempt (should be 0):', count_after)

    # Now set provider available and try again
    provider.availability = 'available'
    provider.save()
    print('Provider availability set to', provider.availability)

    get_resp2 = client.get(f'/booking/{provider.id}/')
    print('GET after available status_code=', get_resp2.status_code)
    post_resp2 = client.post(f'/booking/{provider.id}/', post_data, follow=True)
    print('POST after available status_code=', post_resp2.status_code)
    print('POST after available redirects to:', getattr(post_resp2, 'redirect_chain', None))

    count_final = Booking.objects.filter(provider=provider).count()
    print('Bookings for provider after available attempt (should be 1):', count_final)

except Exception as e:
    print('Error during test run:', e)
    raise

print('Test script finished.')
