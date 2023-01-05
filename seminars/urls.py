
from django.urls import path
from seminars.views import (RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView, 
                            SeminarCreateView, SeminarListView, SeminarUpdateView, SeminarDeleteView,
                            BookingListView, BookingCreateView, BookingDetailView)
from seminars import views


app_name = 'seminars'

urlpatterns = [    
    path("rooms", RoomListView.as_view(), name="room-index"),
    path("rooms/create", RoomCreateView.as_view(), name="room-create"),
    path("rooms/<str:pk>/update", RoomUpdateView.as_view(), name="room-update"),
    path("rooms/<str:pk>/delete", RoomDeleteView.as_view(), name="room-delete"),

    path("seminars", SeminarListView.as_view(), name="seminar-index"),
    path("seminars/create", SeminarCreateView.as_view(), name="seminar-create"),
    path("seminars/<str:pk>/update", SeminarUpdateView.as_view(), name="seminar-update"),
    path("seminars/<str:pk>/delete", SeminarDeleteView.as_view(), name="seminar-delete"),

    path("bookings", BookingListView.as_view(), name="booking-index"),
    path("bookings/<str:seminar_id>", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/result/<str:booking_id>", BookingDetailView.as_view(), name="booking-result"),

]