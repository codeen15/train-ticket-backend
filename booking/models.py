from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)

    class Meta:
        db_table = "locations"

class Trip(models.Model):
    origin = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='origin')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination')
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "trips"

class Booking(models.Model):
    departure_trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='departure_trip')
    return_trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, default=None, related_name='return_trip')
    payment_done = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, default=None)
    email = models.EmailField(null=True, default=None)

    class Meta:
        db_table = "bookings"

class BookedSeats(models.Model):
    seat = models.CharField(max_length=3)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        db_table = "booked_seats"
        unique_together = ('seat', 'trip',)