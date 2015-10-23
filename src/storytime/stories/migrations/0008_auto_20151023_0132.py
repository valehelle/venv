# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_auto_20151021_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]
