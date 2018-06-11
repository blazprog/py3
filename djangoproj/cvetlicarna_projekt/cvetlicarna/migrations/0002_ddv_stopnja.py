# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvetlicarna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddv',
            name='stopnja',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
