# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0012_metric_score_column'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='score_column',
        ),
    ]
