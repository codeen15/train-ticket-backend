# Generated by Django 5.1.1 on 2024-09-29 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='booking.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='booking.location')),
            ],
            options={
                'db_table': 'trips',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_done', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('departure_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_trip', to='booking.trip')),
                ('return_trip', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_trip', to='booking.trip')),
            ],
            options={
                'db_table': 'bookings',
            },
        ),
        migrations.CreateModel(
            name='BookedSeats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(max_length=3)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.trip')),
            ],
            options={
                'db_table': 'booked_seats',
                'unique_together': {('seat', 'trip')},
            },
        ),
    ]
