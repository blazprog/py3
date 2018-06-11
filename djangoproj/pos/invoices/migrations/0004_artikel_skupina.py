# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_skupinaartikla'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikel',
            name='skupina',
            field=models.ForeignKey(default=1, to='invoices.SkupinaArtikla'),
            preserve_default=False,
        ),
    ]
