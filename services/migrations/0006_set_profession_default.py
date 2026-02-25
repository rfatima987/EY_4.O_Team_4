from django.db import migrations, models


def set_default_profession(apps, schema_editor):
    ServiceProvider = apps.get_model('services', 'ServiceProvider')
    # Set profession to 'General' where empty or null
    ServiceProvider.objects.filter(models.Q(profession='') | models.Q(profession__isnull=True)).update(profession='General')


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_experience_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='profession',
            field=models.CharField(max_length=50, default='General', blank=True),
        ),
        migrations.RunPython(set_default_profession, migrations.RunPython.noop),
    ]
