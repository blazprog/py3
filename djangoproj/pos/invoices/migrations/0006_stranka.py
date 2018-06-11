# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_counter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stranka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
    ]
