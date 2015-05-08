# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0003_auto_20150419_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='severity',
            field=models.FloatField(default=1.0, choices=[(1.5, 'High (1.5x)'), (1.0, 'Normal (1.0x)'), (0.5, 'Low (0.5x)')]),
        ),
    ]
