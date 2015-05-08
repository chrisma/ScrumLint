# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0014_dailyuserstorythroughput'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
