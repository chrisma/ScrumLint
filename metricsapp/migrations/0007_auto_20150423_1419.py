# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0006_metric_result_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metric',
            old_name='result_json',
            new_name='results',
        ),
    ]
