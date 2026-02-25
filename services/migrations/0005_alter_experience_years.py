from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_serviceprovider_aadhar_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='experience_years',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
