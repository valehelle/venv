# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storytime.stories.models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='i_path',
            field=models.FileField(upload_to=storytime.stories.models.get_upload_file_name),
        ),
    ]
