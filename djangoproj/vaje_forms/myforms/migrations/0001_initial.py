# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExercisesModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('exercise', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('language', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('subject', models.CharField(max_length=60)),
                ('language', models.ForeignKey(to='myforms.Language')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exercisesmodel',
            name='language',
            field=models.ForeignKey(to='myforms.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercisesmodel',
            name='subject',
            field=models.ForeignKey(to='myforms.Subject'),
            preserve_default=True,
        ),
    ]
