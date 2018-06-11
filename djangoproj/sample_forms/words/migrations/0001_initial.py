# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('word', models.CharField(max_length=70)),
                ('translation', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('sample_use', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
