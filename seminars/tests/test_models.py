from django.test import TestCase
from datetime import datetime
from pytz import UTC
from seminars.models import SEMINAR_STATUS, Room, Seminar, Booking
from portal.models import User
from django.utils.crypto import get_random_string

class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )

    def test_no(self):
        room = Room.objects.get(no='Test Room 1')
        no = room.no
        self.assertEqual(no, 'Test Room 1')

    def test_desc(self):
        room = Room.objects.get(no='Test Room 1')
        desc = room.desc
        self.assertEqual(desc, 'Test Room 1 Description')

class SeminarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )
        Seminar.objects.create(
            topic='Test Topic 1', 
            start_date_time=datetime(2021, 12, 15, 10, 00, 00, tzinfo=UTC), 
            end_date_time=datetime(2021, 12, 15, 11, 00, 00, tzinfo=UTC),
            venue=room,
            no_of_available_seat=20,
            status='OP',
            created_by=user,
        )

    def test_topic(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        topic = seminar.topic
        self.assertEqual(topic, 'Test Topic 1')

    def test_venue(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        room_id = Room.objects.last().id
        room = Room.objects.get(id=room_id)
        venue = seminar.venue
        self.assertEqual(venue, room)

    def test_no_of_available_seat(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        no_of_available_seat = seminar.no_of_available_seat
        self.assertEqual(no_of_available_seat, 20)

    def test_start_date_time(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        start_date_time = seminar.start_date_time
        self.assertEqual(start_date_time, datetime(2021, 12, 15, 10, 00, 00, tzinfo=UTC))

    def test_end_date_time(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        end_date_time = seminar.end_date_time
        self.assertEqual(end_date_time, datetime(2021, 12, 15, 11, 00, 00, tzinfo=UTC))
    
    def test_status(self):
        seminar_id = Seminar.objects.last().id
        seminar = Seminar.objects.get(id=seminar_id)
        status = seminar.status
        self.assertEqual(status, 'OP')

class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )
        seminar = Seminar.objects.create(
            topic='Test Topic 1', 
            start_date_time=datetime(2021, 12, 15, 10, 00, 00, tzinfo=UTC), 
            end_date_time=datetime(2021, 12, 15, 11, 00, 00, tzinfo=UTC),
            venue=room,
            no_of_available_seat=20,
            status='OP',
            created_by=user,
        )        
        Booking.objects.create(
            seminar=seminar,
            attendee=user,
            unique_string=get_random_string(length=32),
            created_by=user,
        )

    def test_seminar(self):
        booking_id = Booking.objects.last().id
        seminar_id = Seminar.objects.last().id
        booking = Booking.objects.get(id=booking_id)
        seminar = Seminar.objects.get(id=seminar_id)
        booking_seminar = booking.seminar
        self.assertEqual(seminar, booking_seminar)

