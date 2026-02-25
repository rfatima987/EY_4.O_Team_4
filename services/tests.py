from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ServiceProvider, Booking, Review


class ReviewTests(TestCase):
	def setUp(self):
		# Create provider user and provider
		self.provider_user = User.objects.create_user(username='prov', email='prov@example.com', password='provpass')
		self.provider = ServiceProvider.objects.create(user=self.provider_user, name='Prov', email='prov@example.com', profession='General', experience_years=2)

		# Create customer
		self.customer = User.objects.create_user(username='cust', email='cust@example.com', password='custpass')

		# Create a completed booking
		self.booking = Booking.objects.create(provider=self.provider, customer_user=self.customer, customer_name='Cust', customer_phone='9999999999', customer_address='Addr', service='repair', booking_date='2025-01-01', booking_time='10:00', status='completed')

		self.client = Client()

	def test_submit_review_success_and_rating_agg(self):
		self.client.login(username='cust', password='custpass')
		url = reverse('submit_review')
		resp = self.client.post(url, {'booking_id': self.booking.id, 'provider_id': self.provider.id, 'rating': 5, 'comment': 'Great work'})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertTrue(data.get('success'))

		# Review exists
		self.assertTrue(Review.objects.filter(booking=self.booking).exists())
		self.provider.refresh_from_db()
		self.assertAlmostEqual(float(self.provider.rating), 5.0, places=2)

	def test_prevent_duplicate_review(self):
		self.client.login(username='cust', password='custpass')
		url = reverse('submit_review')
		resp1 = self.client.post(url, {'booking_id': self.booking.id, 'provider_id': self.provider.id, 'rating': 4, 'comment': 'Good'})
		self.assertEqual(resp1.status_code, 200)
		resp2 = self.client.post(url, {'booking_id': self.booking.id, 'provider_id': self.provider.id, 'rating': 3, 'comment': 'Update'})
		self.assertEqual(resp2.status_code, 400)
		self.assertIn('error', resp2.json())

	def test_cannot_review_non_owner_or_non_completed(self):
		# Not the booking owner
		other = User.objects.create_user(username='other', password='otherpass')
		self.client.login(username='other', password='otherpass')
		url = reverse('submit_review')
		resp = self.client.post(url, {'booking_id': self.booking.id, 'provider_id': self.provider.id, 'rating': 5, 'comment': 'x'})
		self.assertEqual(resp.status_code, 403)

		# Booking not completed
		self.booking.status = 'approved'
		self.booking.save()
		self.client.login(username='cust', password='custpass')
		resp2 = self.client.post(url, {'booking_id': self.booking.id, 'provider_id': self.provider.id, 'rating': 5, 'comment': 'x'})
		self.assertEqual(resp2.status_code, 400)
