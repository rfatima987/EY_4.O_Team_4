import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
django.setup()
from django.contrib.auth.models import User
from services.models import ServiceProvider, Booking

print('USERS:')
for u in User.objects.all():
    print(u.id, u.username, u.email, u.first_name, u.last_name)

print('\nSERVICE PROVIDERS:')
for p in ServiceProvider.objects.all():
    print(p.id, p.name, p.email, 'user_id=' + str(p.user_id), 'total_jobs=' + str(p.total_jobs))

print('\nBOOKINGS:')
for b in Booking.objects.select_related('provider','customer_user').all():
    print(b.id, 'provider_id=', b.provider_id, 'provider_name=', b.provider.name, 'status=', b.status, 'customer_user_id=', b.customer_user_id, 'customer_name=', b.customer_name)

print('\nProviders without linked user but with bookings:')
for p in ServiceProvider.objects.filter(user__isnull=True):
    has_bookings = Booking.objects.filter(provider=p).exists()
    if has_bookings:
        print('Provider', p.id, p.name, p.email, 'has bookings')

print('\nBookings whose provider has no user link:')
for b in Booking.objects.filter(provider__user__isnull=True).select_related('provider')[:20]:
    print('Booking', b.id, 'provider', b.provider.id, b.provider.name, 'status', b.status)

print('\nUser<->Provider email matches:')
for u in User.objects.exclude(email=''):
    matches = ServiceProvider.objects.filter(email__iexact=u.email)
    if matches.exists():
        print('User', u.id, u.email, 'matches providers:', [ (m.id,m.name) for m in matches ])

print('\nDone')
