# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedPosition',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('time', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('accuracy', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrackingKey',
            fields=[
                ('key', models.CharField(primary_key=True, serialize=False, max_length=32)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrackingSession',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ViewKey',
            fields=[
                ('key', models.CharField(primary_key=True, serialize=False, max_length=32)),
                ('session', models.OneToOneField(to='tracker.TrackingSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='trackedposition',
            name='session',
            field=models.ForeignKey(to='tracker.TrackingSession'),
            preserve_default=True,
        ),
    ]
