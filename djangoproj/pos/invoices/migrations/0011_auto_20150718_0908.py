# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0010_artikel_davek'),
    ]

    operations = [
        migrations.AddField(
            model_name='racunpozicija',
            name='txtNazivArtikla',
            field=models.CharField(max_length=25, default='naziv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='racunpozicija',
            name='txtSifraArtikla',
            field=models.CharField(max_length=5, default='sifra'),
            preserve_default=False,
        ),
    ]
