# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20150405_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackingsession',
            name='is_cleaned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
