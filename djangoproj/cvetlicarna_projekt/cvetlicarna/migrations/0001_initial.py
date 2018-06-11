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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nazivArtikla', models.CharField(max_length=100)),
                ('cena', models.FloatField(default=0)),
                ('dolgiOpis', models.TextField()),
                ('slika', models.ImageField(upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DDV',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('naziv', models.CharField(max_length=5)),
                ('dolgiNaziv', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Drzava',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('oznaka', models.CharField(max_length=5)),
                ('naziv', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Em',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('naziv', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('postnaStevilka', models.CharField(max_length=20)),
                ('naziv', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stranka',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nazivStranke', models.CharField(max_length=60)),
                ('ulica', models.CharField(max_length=60)),
                ('kraj', models.CharField(max_length=60)),
                ('idDrzava', models.ForeignKey(to='cvetlicarna.Drzava')),
                ('idPosta', models.ForeignKey(to='cvetlicarna.Posta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VrstaArtikla',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('naziv', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='artikel',
            name='idDDV',
            field=models.ForeignKey(to='cvetlicarna.DDV'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artikel',
            name='idEm',
            field=models.ForeignKey(to='cvetlicarna.Em'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='artikel',
            name='idVrstaArtikla',
            field=models.ForeignKey(to='cvetlicarna.VrstaArtikla'),
            preserve_default=True,
        ),
    ]
