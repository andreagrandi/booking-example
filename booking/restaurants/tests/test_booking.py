from django.test import TestCase
from datetime import datetime
import pytz
from .factories import RestaurantFactory, TableFactory, BookingFactory
from restaurants import booking


class ModelsTest(TestCase):
    def setUp(self):
        self.restaurant_1 = RestaurantFactory.create(opening_time=18, closing_time=23)
        self.restaurant_1_table_1 = TableFactory.create(restaurant=self.restaurant_1, size=2)
        self.restaurant_1_table_2 = TableFactory.create(restaurant=self.restaurant_1, size=4)
        self.booking_1 = BookingFactory.create(
            table=self.restaurant_1_table_2,
            people=4,
            booking_date_time=datetime(2015, 2, 14, 19, 0, tzinfo=pytz.UTC))

    def test_get_first_table_available(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 20, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table.id, self.restaurant_1_table_1.id)

    def test_get_first_table_available_unavailable(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 20, 0, tzinfo=pytz.UTC),
            people=4)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_closing(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 22, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table, None)

    def test_unavailable_tables_1_hour_before_opening(self):
        table = booking.get_first_table_available(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 17, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(table, None)

    def test_book_first_available_table(self):
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 20, 0, tzinfo=pytz.UTC),
            people=2)
        self.assertEqual(booking_response['table'], self.restaurant_1_table_1.id)

    def test_get_expected_diners(self):
        self.booking_2 = BookingFactory.create(
            table=self.restaurant_1_table_1,
            people=2,
            booking_date_time=datetime(2015, 2, 14, 19, 0, tzinfo=pytz.UTC))
        diners = booking.get_expected_diners(self.restaurant_1,
            datetime(2015, 2, 14, tzinfo=pytz.UTC))
        self.assertEqual(diners, 6)

    def test_book_table_for_2_hours(self):
        booking_response = booking.book_restaurant_table(
            restaurant=self.restaurant_1,
            booking_date_time=datetime(2015, 2, 14, 21, 0, tzinfo=pytz.UTC),
            people=2,
            minutes_slot=120)
        self.assertEqual(booking_response['table'], self.restaurant_1_table_1.id)
