from rest_framework import serializers


class GetTrainSerializer(serializers.Serializer):
    origin_id = serializers.IntegerField(write_only=True)
    destination_id = serializers.IntegerField(write_only=True)
    date = serializers.DateField(write_only=True)

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    short_name = serializers.CharField()

class TrainTripSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    origin_id = serializers.IntegerField(write_only=True)
    destination_id = serializers.IntegerField(write_only=True)
    date_time = serializers.DateTimeField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_seat = serializers.IntegerField(read_only=True, required=False)

class BookingSerializer(serializers.Serializer):
    departure_trip_id = serializers.IntegerField(write_only=True)
    departure_trip = TrainTripSerializer(read_only=True)
    departure_seats = serializers.ListField(child=serializers.CharField(), required=True)
    return_trip_id = serializers.IntegerField(required=False, write_only=True)
    return_trip = TrainTripSerializer(required=False, read_only=True)
    return_seats = serializers.ListField(child=serializers.CharField(), required=False)
    payment_done = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

class PaymentSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    booking_id = serializers.IntegerField()