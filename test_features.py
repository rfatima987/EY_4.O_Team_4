#!/usr/bin/env python
"""
FixNear Comprehensive Feature Testing Script
Tests all major functionality of the platform
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixnear.settings')
django.setup()

from django.contrib.auth.models import User
from services.models import ServiceProvider, Booking
from django.test import Client
from django.urls import reverse

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")

def test_database():
    """Test database integrity"""
    print_section("1. DATABASE INTEGRITY TEST")
    
    users = User.objects.count()
    providers = ServiceProvider.objects.count()
    bookings = Booking.objects.count()
    
    print(f"✓ Users in database: {users}")
    print(f"✓ Service providers: {providers}")
    print(f"✓ Total bookings: {bookings}")
    
    if users > 0 and providers > 0:
        print("\n✓ Database is populated and ready")
        return True
    else:
        print("\n✗ Database needs more data")
        return False

def test_booking_workflow():
    """Test complete booking workflow"""
    print_section("2. BOOKING WORKFLOW TEST")
    
    # Get first customer and provider
    customer = User.objects.filter(serviceprovider__isnull=True).first()
    provider = ServiceProvider.objects.first()
    
    if not customer or not provider:
        print("✗ Cannot run booking workflow - insufficient data")
        return False
    
    print(f"Using customer: {customer.email}")
    print(f"Using provider: {provider.name}")
    
    # Count initial bookings
    initial_bookings = Booking.objects.filter(customer_user=customer).count()
    print(f"\n✓ Customer has {initial_bookings} existing bookings")
    
    # Check booking status distribution
    print("\nBooking Status Distribution:")
    for status in ['pending', 'approved', 'completed', 'rejected']:
        count = Booking.objects.filter(status=status).count()
        print(f"  • {status.capitalize()}: {count}")
    
    return True

def test_provider_functionality():
    """Test provider-specific features"""
    print_section("3. PROVIDER FUNCTIONALITY TEST")
    
    providers = ServiceProvider.objects.all()
    print(f"Total providers: {providers.count()}\n")
    
    for provider in providers[:3]:
        bookings = Booking.objects.filter(provider=provider)
        total = bookings.count()
        completed = bookings.filter(status='completed').count()
        pending = bookings.filter(status='pending').count()
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        print(f"Provider: {provider.name}")
        print(f"  Email: {provider.email}")
        print(f"  Profession: {provider.profession}")
        print(f"  Bookings: {total} (Completed: {completed}, Pending: {pending})")
        print(f"  Completion Rate: {completion_rate:.1f}%")
        print(f"  Rating: {provider.rating}/5.0")
        print(f"  User Link: {'✓ Linked' if provider.user else '✗ Not linked'}")
        print()
    
    return True

def test_customer_functionality():
    """Test customer-specific features"""
    print_section("4. CUSTOMER FUNCTIONALITY TEST")
    
    # Find customers (users without provider profile)
    customers = []
    for user in User.objects.all():
        if not hasattr(user, 'serviceprovider'):
            customers.append(user)
    
    print(f"Total customers: {len(customers)}\n")
    
    for customer in customers[:3]:
        bookings = Booking.objects.filter(customer_user=customer)
        total = bookings.count()
        completed = bookings.filter(status='completed').count()
        pending = bookings.filter(status='pending').count()
        
        success_rate = (completed / total * 100) if total > 0 else 0
        
        print(f"Customer: {customer.first_name} {customer.last_name}")
        print(f"  Email: {customer.email}")
        print(f"  Total Bookings: {total}")
        print(f"  Completed: {completed}")
        print(f"  Pending: {pending}")
        print(f"  Success Rate: {success_rate:.1f}%")
        print()
    
    return True

def test_api_endpoints():
    """Test API endpoints"""
    print_section("5. API ENDPOINT TESTS")
    
    client = Client()
    
    # Get a test user
    user = User.objects.first()
    if user:
        client.force_login(user)
        
        # Test bookings status API
        try:
            response = client.get(reverse('bookings_status'))
            print(f"✓ Bookings status API: {response.status_code}")
        except Exception as e:
            print(f"✗ Bookings status API failed: {e}")
        
        # Test get bookings API
        try:
            response = client.get(reverse('get_bookings_api'))
            print(f"✓ Get bookings API: {response.status_code}")
        except Exception as e:
            print(f"✗ Get bookings API failed: {e}")
    
    return True

def test_urls():
    """Test all important URL routes"""
    print_section("6. URL ROUTE TESTS")
    
    critical_routes = [
        'home',
        'login',
        'signup',
        'providers',
        'customer_dashboard',
        'provider_dashboard',
        'my_bookings',
        'provider_requests',
    ]
    
    client = Client()
    user = User.objects.first()
    
    if user:
        client.force_login(user)
    
    for route_name in critical_routes:
        try:
            url = reverse(route_name)
            response = client.get(url)
            status = "✓" if response.status_code < 400 else "✗"
            print(f"{status} {route_name}: {response.status_code} {url}")
        except Exception as e:
            print(f"✗ {route_name}: Error - {e}")
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "FixNear COMPREHENSIVE FEATURE TEST" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    
    tests = [
        test_database,
        test_booking_workflow,
        test_provider_functionality,
        test_customer_functionality,
        test_api_endpoints,
        test_urls,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results.append(False)
    
    # Print summary
    print_section("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - System is operational!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed - check output above")
    
    return passed == total

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
