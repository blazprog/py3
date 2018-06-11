# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_stranka'),
    ]

    operations = [
        migrations.CreateModel(
            name='Racun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('stevilka', models.IntegerField(default=0)),
                ('datum_izdaje', models.DateField()),
                ('kraj_izdaje', models.CharField(max_length=50)),
                ('datum_valute', models.DateField()),
                ('datum_storitve', models.DateField()),
                ('prodajni_pogoji', models.CharField(max_length=50)),
                ('referenca', models.CharField(max_length=50)),
                ('stranka', models.ForeignKey(to='invoices.Stranka')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RacunPozicija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('zaporedna_stevilka', models.IntegerField()),
                ('kolicina', models.FloatField(default=1)),
                ('cena', models.FloatField(default=0)),
                ('davek', models.FloatField(default=0)),
                ('popust', models.FloatField(default=0)),
                ('artikel', models.ForeignKey(to='invoices.Artikel')),
                ('racun', models.ForeignKey(to='invoices.Racun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
