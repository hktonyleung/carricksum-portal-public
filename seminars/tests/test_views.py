from django.test import TestCase
from django.urls import reverse

from seminars.models import Room, Seminar, Booking, SEMINAR_STATUS
from portal.models import User

from datetime import datetime
from pytz import UTC

from http import HTTPStatus

class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_rooms = 3

        user = User.objects.create_superuser(username='testuser', password='123456')

        for room_id in range(number_of_rooms):
            Room.objects.create(
                no=f'Room No {room_id}', 
                desc=f'Room No {room_id} Description', 
                created_by=user,
            )

    def test_room_list_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/seminars/rooms')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostListView
    def test_room_list_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('seminars:room-index'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check we used correct template
        self.assertTemplateUsed(response, 'seminars/room_index.html')

        self.assertEqual(len(response.context['rooms']), 3)  

    # Test RoomDetailView 
    def test_room_detail_view_if_not_logged_in(self):
        response = self.client.get('/seminars/rooms/1/update')
        self.assertRedirects(response, '/no-permission')

class SeminarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests

        user = User.objects.create_superuser(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )
        seminar = Seminar.objects.create(
            topic='Test Topic 1', 
            start_date_time=datetime(2022, 12, 15, 10, 00, 00, tzinfo=UTC), 
            end_date_time=datetime(2022, 12, 15, 11, 00, 00, tzinfo=UTC),
            venue=room,
            no_of_available_seat=20,
            status='OP',
            created_by=user,
        )

    def test_seminar_create(self):
        login = self.client.login(username='testuser', password='123456')
        room = Room.objects.get(id=Room.objects.last().id)
        response = self.client.post('/seminars/seminars/create', {
                'topic': 'Test Seminar 2', 
                'start_date_time':'2022-12-20T10:00:00',
                'end_date_time':'2022-12-20T11:00:00',
                'no_of_available_seat':'10',
                'venue': room.id})

        no_of_seminar = Seminar.objects.count()
        self.assertEqual(no_of_seminar, 2)

    def test_seminar_update(self):
        login = self.client.login(username='testuser', password='123456')
        seminar_id=Seminar.objects.last().id
        seminar = Seminar.objects.last()
        response = self.client.post('/seminars/seminars/'+ str(seminar_id) +'/update', {
                'topic': 'Test Seminar 1 Updated', 
                'start_date_time':'2022-12-23T10:00:00',
                'end_date_time':'2022-12-23T11:00:00',
                'no_of_available_seat':'10',
                'venue': seminar.venue.id})
        seminar = Seminar.objects.get(id=seminar_id)
        topic = seminar.topic
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(topic, 'Test Seminar 1 Updated')
        
    def test_seminar_delete(self):
        login = self.client.login(username='testuser', password='123456')
        seminar_id=Seminar.objects.last().id
        response = self.client.post('/seminars/seminars/'+ str(seminar_id) + '/delete')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        no_of_seminar = Seminar.objects.count()
        self.assertEqual(no_of_seminar, 0)

class BookingViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )
        seminar = Seminar.objects.create(
            topic='Test Topic 1', 
            start_date_time=datetime(2022, 12, 15, 10, 00, 00, tzinfo=UTC), 
            end_date_time=datetime(2022, 12, 15, 11, 00, 00, tzinfo=UTC),
            venue=room,
            no_of_available_seat=20,
            status='OP',
            created_by=user,
        )

    def test_booking_create(self):
        login = self.client.login(username='testuser', password='123456')
        seminar_id = Seminar.objects.last().id
        response = self.client.post('/seminars/bookings/1' , {
                'seminar_id': seminar_id})
        no_of_booking = Booking.objects.count()
        self.assertEqual(no_of_booking, 1)
        booking_id = Booking.objects.last().id
        booking = Booking.objects.get(id=booking_id)
        self.assertRedirects(response, reverse('seminars:booking-result', args=[booking.id]))