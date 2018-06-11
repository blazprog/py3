# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myforms', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='group',
            field=models.CharField(max_length=30, default='top', blank=True),
            preserve_default=False,
        ),
    ]
