# Generated manually for Provider and DeviceGroup models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_add_uuid_to_site'),
    ]

    operations = [
        # Create Provider model
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'providers',
                'ordering': ['name'],
            },
        ),
        # Create DeviceGroup model
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'device_groups',
                'ordering': ['name'],
            },
        ),
        # Add provider foreign key to Device
        migrations.AddField(
            model_name='device',
            name='provider',
            field=models.ForeignKey(
                blank=True,
                db_column='provider_id',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='devices',
                to='api.provider'
            ),
        ),
        # Add device_group foreign key to Device
        migrations.AddField(
            model_name='device',
            name='device_group',
            field=models.ForeignKey(
                blank=True,
                db_column='device_group_id',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='devices',
                to='api.devicegroup'
            ),
        ),
    ]
