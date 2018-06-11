# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='cena',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artikel',
            name='em',
            field=models.CharField(max_length=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artikel',
            name='naziv',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artikel',
            name='sifra',
            field=models.CharField(max_length=5),
            preserve_default=True,
        ),
    ]
