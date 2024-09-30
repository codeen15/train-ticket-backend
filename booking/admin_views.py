from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response

from booking.models import BookedSeats, Booking, Location, Trip
from booking.serializers import BookingSerializer, LocationSerializer, TrainTripSerializer


class LocationView(APIView):

    def get(self, request):
        
        locations = Location.objects.all()

        serializer = LocationSerializer(locations, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        name = data.get("name")
        short_name = data.get("short_name")

        location = Location.objects.create(
            name=name,
            short_name=short_name
        )

        serializer = LocationSerializer(location)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        if id is None:
            return Response(data={
                "message": "Invalid id"
            })

        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        name = data.get("name")
        short_name = data.get("short_name")

        location = Location.objects.filter(id=id).first()
        if not location:
            return Response(data={
                "message": "Invalid id"
            })
        
        location.name = name
        location.short_name = short_name
        location.save()

        serializer = LocationSerializer(location)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        if id is None:
            return Response(data={
                "message": "Invalid id"
            })
        
        location = Location.objects.filter(id=id).first()
        if not location:
            return Response(data={
                "message": "Invalid id"
            })

        location.delete()
        
        return Response(data={
            "message": "Deleted"
        }, status=status.HTTP_200_OK)

class TripView(APIView):

    def get(self, request):
        
        trips = Trip.objects.all()

        serializer = TrainTripSerializer(trips, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TrainTripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        origin_id = data.get("origin_id")
        destination_id = data.get("destination_id")
        date_time = data.get("date_time")
        price = data.get("price")

        trip = Trip.objects.create(
            origin_id=origin_id,
            destination_id=destination_id,
            date_time=date_time,
            price=price
        )

        serializer = TrainTripSerializer(trip)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        if id is None:
            return Response(data={
                "message": "Invalid id"
            })
        
        trip = Trip.objects.filter(id=id).first()
        if not trip:
            return Response(data={
                "message": "Invalid id"
            })

        trip.delete()
        
        return Response(data={
            "message": "Deleted"
        }, status=status.HTTP_200_OK)

class BookingView(APIView):

    def get(self, request):
        
        bookings = Booking.objects.all()

        for booking in bookings:
            departure_seats = BookedSeats.objects.filter(booking=booking, trip=booking.departure_trip).all()
            booking.departure_seats = [seat.seat for seat in departure_seats]

            return_seats = BookedSeats.objects.filter(booking=booking, trip=booking.return_trip).all()
            booking.return_seats = [seat.seat for seat in return_seats]
        
        serializer = BookingSerializer(bookings, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)