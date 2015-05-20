# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_date_time',
            new_name='booking_date_time_start',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_date_time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 10, 16, 39, 467711, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
