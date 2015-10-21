# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0006_remove_story_storyid'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='username',
            field=models.CharField(default=55, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='text',
            name='username',
            field=models.CharField(default=32, max_length=50),
            preserve_default=False,
        ),
    ]
