# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TujaBeseda',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('beseda', models.CharField(max_length=120)),
                ('opis', models.TextField()),
                ('uporaba', models.TextField()),
                ('prevod', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
