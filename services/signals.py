"""
Django signals for booking-related notifications and events.
Tracks booking status changes, sends notifications, and updates provider statistics.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Booking, ServiceProvider
from django.contrib import messages


@receiver(pre_save, sender=Booking)
def track_booking_status_change(sender, instance, **kwargs):
    """
    Track booking status changes for notifications.
    Called before booking is saved.
    """
    try:
        old_booking = Booking.objects.get(pk=instance.pk)
        instance._old_status = old_booking.status
    except Booking.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Booking)
def handle_booking_status_change(sender, instance, created, **kwargs):
    """
    Handle booking status changes - update provider stats, etc.
    Called after booking is saved.
    """
    if created:
        # New booking created
        # Could send welcome email to customer, notification to provider
        pass
    else:
        # Booking updated
        old_status = getattr(instance, '_old_status', None)
        new_status = instance.status
        
        if old_status and old_status != new_status:
            # Status changed
            if new_status == 'approved' and old_status == 'pending':
                # Booking approved - could send approval email to customer
                pass
            elif new_status == 'rejected' and old_status == 'pending':
                # Booking rejected - could send rejection email to customer
                pass
            elif new_status == 'completed':
                # Booking completed - could send review request
                pass
            elif new_status == 'cancelled':
                # Booking cancelled - could send cancellation email
                pass


@receiver(post_save, sender=ServiceProvider)
def update_provider_ratings(sender, instance, **kwargs):
    """
    Update provider completion rates and statistics.
    Called when ServiceProvider is saved.
    """
    # This could calculate average rating from reviews if reviews table exists
    # Or update completion rate based on completed bookings
    pass
