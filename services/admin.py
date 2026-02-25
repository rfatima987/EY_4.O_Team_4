from django.contrib import admin
from .models import ServiceProvider, Booking

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'profession', 
        'city', 
        'verified_status',
        'aadhar_status',
        'certificate_status',
        'rating', 
        'total_jobs'
    ]
    
    list_filter = [
        'verified',
        'city',
        'profession',
        'created_at',
    ]
    
    search_fields = ['name', 'email', 'phone', 'aadhar_number']
    
    fieldsets = (
        ('User Link', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'bio', 'avatar_url')
        }),
        ('Professional Details', {
            'fields': ('profession', 'service_type', 'experience_years')
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'address')
        }),
        ('Pricing', {
            'fields': ('hourly_rate', 'call_charge')
        }),
        ('Verification & Status', {
            'fields': ('aadhar_number', 'certificate', 'verified', 'availability')
        }),
        ('Statistics', {
            'fields': ('rating', 'total_jobs', 'member_since', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'member_since', 'total_jobs']
    
    actions = ['mark_verified', 'mark_unverified', 'download_certificates']
    
    def verified_status(self, obj):
        """Display verification status with color."""
        if obj.verified:
            return '✓ Verified'
        else:
            return '✗ Pending'
    verified_status.short_description = 'Verification Status'
    
    def aadhar_status(self, obj):
        """Show if aadhar is uploaded."""
        if obj.aadhar_number:
            return f'✓ {obj.aadhar_number[:4]}...' if len(obj.aadhar_number) > 4 else '✓ Present'
        else:
            return '✗ Missing'
    aadhar_status.short_description = 'Aadhar'
    
    def certificate_status(self, obj):
        """Show if certificate is uploaded."""
        if obj.certificate:
            return f'✓ {obj.certificate.name.split("/")[-1][:20]}...'
        else:
            return '✗ Missing'
    certificate_status.short_description = 'Certificate'
    
    @admin.action(description='Mark selected as Verified')
    def mark_verified(self, request, queryset):
        """Admin action to mark providers as verified."""
        updated = queryset.update(verified=True)
        self.message_user(request, f'{updated} provider(s) marked as verified.')
    
    @admin.action(description='Mark selected as Unverified')
    def mark_unverified(self, request, queryset):
        """Admin action to mark providers as unverified."""
        updated = queryset.update(verified=False)
        self.message_user(request, f'{updated} provider(s) marked as unverified.')
    
    @admin.action(description='Download certificates of selected')
    def download_certificates(self, request, queryset):
        """Show message that admin can download from file system."""
        count = queryset.filter(certificate__isnull=False).exclude(certificate='').count()
        self.message_user(request, f'{count} certificate(s) available for download in /media/certificates/ directory.')

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_name',
        'provider',
        'service',
        'booking_date',
        'status',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'booking_date',
        'created_at',
        'provider__city',
    ]
    
    search_fields = ['customer_name', 'provider__name', 'service']
    readonly_fields = ['created_at', 'updated_at']
    
    fields = [
        'provider',
        'customer_user',
        'customer_name',
        'customer_phone',
        'customer_email',
        'customer_address',
        'service',
        'booking_date',
        'booking_time',
        'notes',
        'status',
        'created_at',
        'updated_at'
    ]

admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Booking, BookingAdmin)