# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0004_metric_severity'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
