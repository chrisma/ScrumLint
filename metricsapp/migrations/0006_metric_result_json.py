# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0005_metric_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='result_json',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
