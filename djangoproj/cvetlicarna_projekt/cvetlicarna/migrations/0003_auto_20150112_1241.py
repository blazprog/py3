# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvetlicarna', '0002_ddv_stopnja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='slika',
            field=models.ImageField(blank=True, upload_to='', null=True),
            preserve_default=True,
        ),
    ]
