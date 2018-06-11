# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisesmodel',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercisesmodel',
            name='subject',
            field=models.CharField(blank=True, max_length=60, null=True),
            preserve_default=True,
        ),
    ]
