from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ServiceProvider, Booking
from datetime import date, time

class Command(BaseCommand):
    help = 'Create test provider, customer and a booking'

    def handle(self, *args, **options):
        p_email='test_provider@example.com'
        provider_user, created = User.objects.get_or_create(username='test_provider', defaults={'email':p_email,'first_name':'Test','last_name':'Provider'})
        if created:
            provider_user.set_password('password123')
            provider_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created provider user {provider_user.email}'))
        else:
            self.stdout.write(f'Provider user exists {provider_user.email}')

        c_email='test_customer@example.com'
        customer_user, created = User.objects.get_or_create(username='test_customer', defaults={'email':c_email,'first_name':'Test','last_name':'Customer'})
        if created:
            customer_user.set_password('password123')
            customer_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created customer user {customer_user.email}'))
        else:
            self.stdout.write(f'Customer user exists {customer_user.email}')

        provider_profile, created = ServiceProvider.objects.get_or_create(email=p_email, defaults={
            'name':'Test Provider','phone':'+911234567890','profession':'General','location':'Test City','city':'Test City','address':'123 Test St'
        })
        if provider_profile.user is None:
            provider_profile.user = provider_user
            provider_profile.save()
            self.stdout.write(self.style.SUCCESS('Linked provider profile to user'))
        else:
            self.stdout.write('Provider profile exists and linked')

        booking = Booking.objects.create(provider=provider_profile, customer_user=customer_user, customer_name=f'{customer_user.first_name} {customer_user.last_name}', customer_phone='+919999999999', customer_email=customer_user.email, customer_address='42 Example Lane', service='Test Service', booking_date=date.today(), booking_time=time(10,30), notes='Test booking', status='pending')
        self.stdout.write(self.style.SUCCESS(f'Created booking id {booking.id}'))
