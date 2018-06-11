# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvetlicarna', '0003_auto_20150112_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Racun',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('stevilkaRacuna', models.IntegerField(default=0)),
                ('datumRacuna', models.DateField(auto_now_add=True)),
                ('krajIzdaje', models.CharField(max_length=60)),
                ('sifraStranke', models.ForeignKey(to='cvetlicarna.Stranka')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RacunPostavka',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('stevilkaPostavke', models.IntegerField(default=0)),
                ('kolicina', models.FloatField()),
                ('cena', models.FloatField()),
                ('popust', models.FloatField()),
                ('idDDv', models.ForeignKey(to='cvetlicarna.DDV')),
                ('idEm', models.ForeignKey(to='cvetlicarna.Em')),
                ('idRacuna', models.ForeignKey(to='cvetlicarna.Racun')),
                ('sifraArtikla', models.ForeignKey(to='cvetlicarna.Artikel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
