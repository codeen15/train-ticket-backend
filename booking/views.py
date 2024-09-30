from datetime import datetime
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from booking.email import send_qr_code_email
from booking.models import BookedSeats, Booking, Location, Trip
from booking.serializers import BookingSerializer, GetTrainSerializer, LocationSerializer, PaymentSerializer, TrainTripSerializer

@api_view(['GET'])
def get_locations(request):
    locations = Location.objects.all()

    serializer = LocationSerializer(locations, many=True)
    
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_train(request):
    serializer = GetTrainSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    origin_id: int = data.get('origin_id')
    destination_id: int = data.get('destination_id')
    date: datetime = data.get('date')

    trips = Trip.objects.filter(
        origin=origin_id,
        destination=destination_id,
        date_time__date=date
    ).annotate(
        available_seat=120 - (Count('departure_trip__bookedseats') + Count('return_trip__bookedseats'))
    )

    serializer = TrainTripSerializer(trips, many=True)
    
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_booked_seats(request, id):

    trip_id = id

    booked_seats = BookedSeats.objects.filter(
        trip_id=trip_id
    ).values('seat')

    seats = []

    for seat in booked_seats:
        seats.append(seat.get('seat'))
    
    return Response(data=seats, status=status.HTTP_200_OK)

@api_view(['POST'])
def confirm_booking(request):

    try:
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        departure_trip_id = data.get("departure_trip_id")
        departure_seats = data.get("departure_seats", [])
        return_trip_id = data.get("return_trip_id", None)
        return_seats = data.get("return_seats", [])


        booking = Booking.objects.create(
            departure_trip_id=departure_trip_id,
            return_trip_id=return_trip_id
        )

        for seat in departure_seats:
            BookedSeats.objects.create(
                seat=seat,
                trip_id=departure_trip_id,
                booking=booking
            )

        for seat in return_seats:
            BookedSeats.objects.create(
                seat=seat,
                trip_id=return_trip_id,
                booking=booking
            )
        
        return Response(data={
            "booking_id": booking.id
        }, status=status.HTTP_200_OK)
    
    except IntegrityError:
        return Response(data={
            "message": "Seat already taken"
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def make_payment(request):

    serializer = PaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    booking_id = data.get("booking_id")
    name = data.get("name")
    email = data.get("email")

    booking = Booking.objects.filter(
        id=booking_id
    ).first()

    booking.name = name
    booking.email = email
    booking.payment_done = True
    booking.save()

    send_qr_code_email(booking.id, booking.name, booking.email)
    
    return Response(data={
        "message": "Payment success"
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def booking_summary(request, booking_id=None):

    if booking_id is None:
        return Response(data={
            "message": "Invalid booking id"
        }, status=status.HTTP_400_BAD_REQUEST)

    booking = Booking.objects.filter(
        id=booking_id
    ).first()

    if not booking:
        return Response(data={
            "message": "Invalid booking id"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    departure_seats = BookedSeats.objects.filter(booking=booking, trip=booking.departure_trip).all()
    booking.departure_seats = [seat.seat for seat in departure_seats]

    return_seats = BookedSeats.objects.filter(booking=booking, trip=booking.return_trip).all()
    booking.return_seats = [seat.seat for seat in return_seats]
    
    serializer = BookingSerializer(booking)
    
    return Response(data=serializer.data, status=status.HTTP_200_OK)