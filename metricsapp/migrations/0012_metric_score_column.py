# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0011_auto_20150427_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='score_column',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
