# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0009_metric_last_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='explanation',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
