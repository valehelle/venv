# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_story_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='storyid',
            field=models.CharField(default=1, unique=True, max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='position',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='story',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='like',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='position',
            field=models.IntegerField(),
        ),
    ]
