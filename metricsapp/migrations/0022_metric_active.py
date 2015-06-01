# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0021_neverendingstory'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
