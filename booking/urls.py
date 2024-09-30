from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('locations/', views.get_locations),
    path('train/', views.get_train),
    path('train/<int:id>/seats/', views.get_booked_seats),
    path('confirm', views.confirm_booking),
    path('payment', views.make_payment),
    path('summary/<int:booking_id>', views.booking_summary),

    path('admin/locations', admin_views.LocationView.as_view()),
    path('admin/locations/<int:id>', admin_views.LocationView.as_view()),
    path('admin/trips', admin_views.TripView.as_view()),
    path('admin/trips/<int:id>', admin_views.TripView.as_view()),
    path('admin/bookings', admin_views.BookingView.as_view()),
]