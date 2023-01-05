from django.test import TestCase
from seminars.forms import RoomForm, SeminarForm, BookingForm
from seminars.forms import (EMPTY_NO_ERROR, EMPTY_DESC_ERROR, LONG_NO_ERROR, LONG_DESC_ERROR, 
                            EMPTY_TOPIC_ERROR, EMPTY_END_DATE_TIME_ERROR, EMPTY_START_DATE_TIME_ERROR, 
                            LONG_TOPIC_ERROR,INVALID_NO_OF_AVAILABLE_SEAT_ERROR, INVALID_SEMINAR_DATE_RANGE_ERROR,
                            INVALID_SEMINAR_START_END_DATETIME_ERROR, SEMINAR_FULL_ERROR)
from portal.models import User
from seminars.models import Room, Seminar
from django.forms.forms import NON_FIELD_ERRORS
from datetime import datetime

start_date_time = datetime(2022, 12, 20, 10, 00, 00, 000)
end_date_time = datetime(2022, 12, 20, 11, 00, 00, 000)

start_date_time2 = datetime(2022, 11, 20, 10, 00, 00, 000)
end_date_time2 = datetime(2022, 11, 20, 11, 00, 00, 000)

class RoomFormTest(TestCase):

    def test_form_valid_for_no(self):
        form = RoomForm(data={'no': '', 'desc':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['no'], [EMPTY_NO_ERROR])
        self.assertEqual(form.errors['desc'], [EMPTY_DESC_ERROR])

    def test_form_valid_for_long_no(self):
        form = RoomForm(
            data={
                'no': '1234567890123456789012345678901234567890123456789', 
                'desc':'12345'}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['no'], [LONG_NO_ERROR])
        
    def test_form_valid_for_long_desc(self):
        form = RoomForm(
            data={
                'no': '12345', 
                'desc':'1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['desc'], [LONG_DESC_ERROR])

class SeminarFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )
        semianr = Seminar.objects.create(
            topic='Test Topic',
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            no_of_available_seat='0',
            venue= room,
            created_by=user
        )

    def test_form_valid_for_empty_value(self):
        form = SeminarForm(            
            data={
                'topic': '', 
                'start_date_time':'',
                'end_date_time':'',})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['topic'], [EMPTY_TOPIC_ERROR])
        self.assertEqual(form.errors['start_date_time'], [EMPTY_START_DATE_TIME_ERROR])
        self.assertEqual(form.errors['end_date_time'], [EMPTY_END_DATE_TIME_ERROR])

    def test_form_valid(self):
        room = Room.objects.get(id=Room.objects.last().id)
        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2021-12-15T10:00:00',
                'end_date_time':'2021-12-15T11:00:00',
                'no_of_available_seat':'100',
                'venue': room})
        self.assertTrue(form.is_valid())

    def test_form_invalid_available_seat(self):
        room = Room.objects.get(id=Room.objects.last().id)
        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2021-12-15T10:00:00',
                'end_date_time':'2021-12-15T11:00:00',
                'no_of_available_seat':'0',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_NO_OF_AVAILABLE_SEAT_ERROR])
            
    def test_form_valid_invalid_seminar_datetime(self):
        room = Room.objects.get(id=Room.objects.last().id)

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T11:05:00',
                'end_date_time':'2022-12-20T11:00:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_SEMINAR_START_END_DATETIME_ERROR])

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T11:00:00',
                'end_date_time':'2022-12-20T11:00:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_SEMINAR_START_END_DATETIME_ERROR])

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T09:00:00',
                'end_date_time':'2022-12-20T11:00:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_SEMINAR_DATE_RANGE_ERROR])

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T10:15:00',
                'end_date_time':'2022-12-20T10:45:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_SEMINAR_DATE_RANGE_ERROR])

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T10:30:00',
                'end_date_time':'2022-12-20T11:15:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertFalse(form.is_valid())
        errors = form.non_field_errors()
        for error in errors:
            self.assertEqual([error], [INVALID_SEMINAR_DATE_RANGE_ERROR])       

        form = SeminarForm(            
            data={
                'topic': 'Test Seminar', 
                'start_date_time':'2022-12-20T09:00:00',
                'end_date_time':'2022-12-20T10:00:00',
                'no_of_available_seat':'10',
                'venue': room})
        self.assertTrue(form.is_valid())

class BookingFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        room = Room.objects.create(
            no='Test Room 1', 
            desc='Test Room 1 Description', 
            created_by=user,
        )

        semianr1 = Seminar.objects.create(
            topic='Test Topic',
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            no_of_available_seat='0',
            venue= room,
            created_by=user
        )

        seminar2 = Seminar.objects.create(
            topic='Test Topic2',
            start_date_time=start_date_time2,
            end_date_time=end_date_time2,
            no_of_available_seat='20',
            venue= room,
            created_by=user
        )

    def test_form_valid_for_empty_seat(self):
        form = BookingForm(            
            data={
                'seminar_id': 1,})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[NON_FIELD_ERRORS], [SEMINAR_FULL_ERROR])

    def test_form_valid(self):
        form = BookingForm(            
            data={
                'seminar_id': 2,})
        self.assertTrue(form.is_valid())
