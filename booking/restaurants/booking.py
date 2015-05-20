from datetime import timedelta
from django.db.models import Sum
from .models import Table, Booking

def book_restaurant_table(restaurant, booking_date_time, people, minutes_slot=90):
    """
    This method uses get_first_table_available to get the first table available, then it
    creates a Booking on the database.
    """
    table = get_first_table_available(restaurant, booking_date_time, people, minutes_slot)

    if table:
        delta = timedelta(seconds=60*minutes_slot)
        booking = Booking(table=table, people=people,
            booking_date_time_start=booking_date_time, booking_date_time_end=booking_date_time + delta)
        booking.save()
        return {'booking': booking.id, 'table': table.id}
    else:
        return None

def get_first_table_available(restaurant, booking_date_time, people, minutes_slot=90):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    # I make sure to check if the tables are not already booked within the time slot required
    # by the new booking
    delta = timedelta(seconds=60*minutes_slot)
    l_bound_time = booking_date_time
    u_bound_time = booking_date_time + delta

    tables_booked_ids = []

    # Exclude tables which start and end booking date includes requested initial booking date_time
    tables_booked = Booking.objects.filter(table__restaurant=restaurant,
        booking_date_time_start__lt=l_bound_time,
        booking_date_time_end__gt=l_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Exclude tables which start and end booking date includes requested ending booking date_time
    tables_booked = Booking.objects.filter(
        booking_date_time_start__lt=u_bound_time,
        booking_date_time_end__gt=u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Exclude tables which booking slots is inside requested booking slot
    tables_booked = Booking.objects.filter(
        booking_date_time_start__gt=l_bound_time,
        booking_date_time_end__lt=u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Exclude tables which include requested booking slot
    tables_booked = Booking.objects.filter(
        booking_date_time_start__lt=l_bound_time,
        booking_date_time_end__gt=u_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # Then I get a list of all the tables, of the needed size, available in that restaurant and
    # I exclude the previous list of unavailable tables. I order the list from the smaller table
    # to the bigger one and I return the first, smaller one, available.
    tables = Table.objects.filter(restaurant=restaurant,
        restaurant__opening_time__lte=booking_date_time.hour,
        restaurant__closing_time__gte=booking_date_time.hour+(minutes_slot / float(60)),
        size__gte=people).exclude(id__in=tables_booked_ids).order_by('size')

    if tables.count() == 0:
        return None
    else:
        return tables[0]

def get_expected_diners(restaurant, booking_date):
    """
    Return the expected number of diners of a restaurant for a specific date.
    """
    diners = Booking.objects.filter(
        table__restaurant=restaurant,
        booking_date_time_start__year=booking_date.year,
        booking_date_time_start__month=booking_date.month,
        booking_date_time_start__day=booking_date.day).aggregate(Sum('people'))
    return diners['people__sum']
