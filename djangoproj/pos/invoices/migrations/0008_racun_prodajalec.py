# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0007_racun_racunpozicija'),
    ]

    operations = [
        migrations.AddField(
            model_name='racun',
            name='prodajalec',
            field=models.CharField(max_length=50, default='blaz'),
            preserve_default=False,
        ),
    ]
