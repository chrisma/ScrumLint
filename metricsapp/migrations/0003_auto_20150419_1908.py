# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0002_metric_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='endpoint',
            field=models.CharField(default='sample endpoint', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metric',
            name='query',
            field=models.CharField(default='sample query', max_length=2000),
            preserve_default=False,
        ),
    ]
