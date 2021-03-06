# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nakup',
            name='datum_nakupa',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='nakup',
            name='trgovina',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nakupizdelki',
            name='cena',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='nakupizdelki',
            name='izdelek',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nakupizdelki',
            name='kolicina',
            field=models.IntegerField(default=1),
        ),
    ]
