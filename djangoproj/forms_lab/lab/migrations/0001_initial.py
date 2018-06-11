# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nakup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('datum_nakupa', models.DateField(help_text='Datun nakupa')),
                ('trgovina', models.CharField(max_length=30, help_text='Trgovina')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NakupIzdelki',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('izdelek', models.CharField(max_length=30, help_text='Izdelek')),
                ('kolicina', models.IntegerField(default=1, help_text='Količina')),
                ('cena', models.FloatField(default=0, help_text='Cena')),
                ('nakup', models.ForeignKey(to='lab.Nakup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
