# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20151020_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 16, 40, 2, 115000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
