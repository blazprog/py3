# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dokumenti', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='racunpozicija',
            old_name='artikel_racun',
            new_name='artikel',
        ),
    ]
