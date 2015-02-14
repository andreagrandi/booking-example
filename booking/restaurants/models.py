from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    size = models.IntegerField()


class Booking(models.Model):
    table = models.ForeignKey(Table)
    people = models.IntegerField()
    booking_date_time = models.DateTimeField()
