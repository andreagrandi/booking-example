# booking-example
A restaurant table booking example in Python/Django

# Running Tests

    cd booking-example/booking/
    ./manage.py test

# Features implemented

* store Restaurants, Tables and Bookings ( https://github.com/andreagrandi/booking-example/blob/master/booking/restaurants/models.py )
* allow booking at a certain restaurant, at a given date/time for a specific number of people ( https://github.com/andreagrandi/booking-example/blob/master/booking/restaurants/booking.py#L5 )
* return a table for the correct size of the party (always returning the smallest one available) ( https://github.com/andreagrandi/booking-example/blob/master/booking/restaurants/booking.py#L68 )
* generate report with expecyed number of diners for a particular day ( https://github.com/andreagrandi/booking-example/blob/master/booking/restaurants/booking.py#L75 )

## Bonus features

* user can book a table for a defined length of time
* Continuous Integration with TravisCI and Coveralls.io for code testing coverage

Continuous integration status
-----------------------------

[![Travis-CI Status](https://secure.travis-ci.org/andreagrandi/booking-example.png?branch=master)](http://travis-ci.org/#!/andreagrandi/booking-example)

[![Coverage Status](https://coveralls.io/repos/andreagrandi/booking-example/badge.svg)](https://coveralls.io/r/andreagrandi/booking-example)
