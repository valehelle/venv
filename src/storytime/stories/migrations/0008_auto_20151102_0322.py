# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_subscriber_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='person',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
