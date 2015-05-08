# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0008_sprintmetric'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='last_query',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
