from services.models import ServiceProvider
p = ServiceProvider.objects.filter(id=1).first()
print('before', p.availability if p else None)
if p:
    p.availability = 'not_available'
    p.save()
    print('after', p.availability)
else:
    print('provider not found')
