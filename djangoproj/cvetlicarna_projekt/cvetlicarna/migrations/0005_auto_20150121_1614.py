# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvetlicarna', '0004_racun_racunpostavka'),
    ]

    operations = [
        migrations.RenameField(
            model_name='racunpostavka',
            old_name='idDDv',
            new_name='idDDV',
        ),
    ]
