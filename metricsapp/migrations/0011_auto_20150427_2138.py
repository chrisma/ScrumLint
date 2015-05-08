# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0010_metric_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='explanation',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
