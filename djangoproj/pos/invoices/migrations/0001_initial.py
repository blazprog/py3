# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('sifra', models.CharField(max_length=5, help_text='Šifra')),
                ('naziv', models.CharField(max_length=25, help_text='Naziv')),
                ('cena', models.FloatField(help_text='Cena', default=0)),
                ('em', models.CharField(max_length=3, help_text='Em')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
