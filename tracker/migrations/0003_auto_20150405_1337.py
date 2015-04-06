# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20150331_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trackedposition',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='trackingsession',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
