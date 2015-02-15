from datetime import timedelta
from .models import Table, Booking

def book_restaurant_table(restaurant, booking_date_time, people, minutes_slot=90):
    """
    This method uses get_first_table_available to get the first table available, then it
    creates a Booking on the database.
    """
    table = get_first_table_available(restaurant, booking_date_time, people, minutes_slot)

    if table:
        booking = Booking(table=table, people=people, booking_date_time=booking_date_time)
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
    l_bound_time = booking_date_time - delta
    u_bound_time = booking_date_time + delta

    # First I get a list of tables booked in that restaurant, within the given time range
    tables_booked = Booking.objects.filter(table__restaurant=restaurant,
        booking_date_time__gt=l_bound_time, booking_date_time__lt=u_bound_time).values('table')
    tables_booked_ids = [x['table'] for x in tables_booked]

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
