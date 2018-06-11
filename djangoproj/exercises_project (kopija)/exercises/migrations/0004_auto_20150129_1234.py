# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0003_language_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='language',
            field=models.ForeignKey(to='exercises.Language', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exercisesmodel',
            name='language',
            field=models.ForeignKey(to='exercises.Language', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exercisesmodel',
            name='subject',
            field=models.ForeignKey(to='exercises.Subject', default=1),
            preserve_default=False,
        ),
    ]
