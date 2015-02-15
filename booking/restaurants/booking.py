from datetime import timedelta
from .models import Table, Booking

def book_restaurant_table(restaurant, people, booking_date_time):
    pass

def get_first_table_available(restaurant, booking_date_time, people, minutes_slot=90):
    delta = timedelta(seconds=60*minutes_slot)
    l_bound_time = booking_date_time - delta
    u_bound_time = booking_date_time + delta

    tables_booked = Booking.objects.filter(table__restaurant=restaurant,
        booking_date_time__gt=l_bound_time, booking_date_time__lt=u_bound_time).values('table')
    tables_booked_ids = [x['table'] for x in tables_booked]

    tables = Table.objects.filter(restaurant=restaurant,
        restaurant__opening_time__lte=booking_date_time.hour,
        restaurant__closing_time__gte=booking_date_time.hour+(minutes_slot / float(60)),
        size__gte=people).exclude(id__in=tables_booked_ids).order_by('size')

    if tables.count() == 0:
        return None
    else:
        return tables[0]
