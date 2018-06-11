# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='my_photos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
