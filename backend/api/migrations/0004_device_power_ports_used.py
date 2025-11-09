# Generated manually for racksum

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_passkey_passkeychallenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='power_ports_used',
            field=models.IntegerField(
                default=1,
                help_text='Number of PDU power ports required (e.g., 2 for dual PSU)',
                validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
