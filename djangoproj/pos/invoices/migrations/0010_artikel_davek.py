# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0009_documentcounter'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikel',
            name='davek',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
