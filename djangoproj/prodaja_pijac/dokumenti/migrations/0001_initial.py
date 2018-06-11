# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sifranti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('num_counts', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('document', models.CharField(max_length=30)),
                ('next_number', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Racun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('stevilka', models.IntegerField(default=0)),
                ('datum_izdaje', models.DateField()),
                ('kraj_izdaje', models.CharField(max_length=50)),
                ('datum_valute', models.DateField()),
                ('datum_storitve', models.DateField()),
                ('prodajalec', models.CharField(max_length=50)),
                ('prodajni_pogoji', models.CharField(max_length=50)),
                ('referenca', models.CharField(max_length=50)),
                ('stranka', models.ForeignKey(related_name='sifranti_stranka', to='sifranti.Stranka')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RacunPozicija',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('zaporedna_stevilka', models.IntegerField()),
                ('txtSifraArtikla', models.CharField(max_length=5)),
                ('txtNazivArtikla', models.CharField(max_length=25)),
                ('kolicina', models.FloatField(default=1)),
                ('cena', models.FloatField(default=0)),
                ('davek', models.FloatField(default=0)),
                ('popust', models.FloatField(default=0)),
                ('artikel_racun', models.ForeignKey(related_name='sifranti_artikel', to='sifranti.Artikel')),
                ('racun', models.ForeignKey(related_name='dokumenti_racun', to='dokumenti.Racun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
