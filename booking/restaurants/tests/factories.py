import factory
from django.utils.timezone import now
from restaurants.models import Restaurant, Table, Booking


class RestaurantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Restaurant

    name = 'Pizzeria Vesuvio'
    description = 'Traditional pizza of Napoli'
    opening_time = 18
    closing_time = 23


class TableFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Table

    restaurant = factory.SubFactory(RestaurantFactory)
    size = 4


class BookingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Booking

    table = factory.SubFactory(TableFactory)
    people = 3
    booking_date_time = now()
