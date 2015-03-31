# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewkey',
            name='session',
        ),
        migrations.DeleteModel(
            name='ViewKey',
        ),
        migrations.AddField(
            model_name='trackingsession',
            name='viewkey',
            field=models.CharField(default='SECRET_KEY', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackingsession',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
