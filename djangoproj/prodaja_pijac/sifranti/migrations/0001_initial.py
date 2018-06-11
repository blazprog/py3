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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('sifra', models.CharField(max_length=5)),
                ('naziv', models.CharField(max_length=25)),
                ('cena', models.FloatField(default=0)),
                ('davek', models.FloatField(default=0)),
                ('em', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num_counts', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentCounter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('stevilka', models.IntegerField(default=0)),
                ('datum_izdaje', models.DateField()),
                ('kraj_izdaje', models.CharField(max_length=50)),
                ('datum_valute', models.DateField()),
                ('datum_storitve', models.DateField()),
                ('prodajalec', models.CharField(max_length=50)),
                ('prodajni_pogoji', models.CharField(max_length=50)),
                ('referenca', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RacunPozicija',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('zaporedna_stevilka', models.IntegerField()),
                ('txtSifraArtikla', models.CharField(max_length=5)),
                ('txtNazivArtikla', models.CharField(max_length=25)),
                ('kolicina', models.FloatField(default=1)),
                ('cena', models.FloatField(default=0)),
                ('davek', models.FloatField(default=0)),
                ('popust', models.FloatField(default=0)),
                ('artikel', models.ForeignKey(to='sifranti.Artikel')),
                ('racun', models.ForeignKey(to='sifranti.Racun')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkupinaArtikla',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('naziv', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stranka',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('sifra', models.CharField(max_length=5)),
                ('naziv', models.CharField(max_length=50)),
                ('posta', models.CharField(max_length=50)),
                ('ulica', models.CharField(max_length=50)),
                ('kraj', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='racun',
            name='stranka',
            field=models.ForeignKey(to='sifranti.Stranka'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artikel',
            name='skupina',
            field=models.ForeignKey(to='sifranti.SkupinaArtikla'),
            preserve_default=True,
        ),
    ]
