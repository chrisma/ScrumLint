# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0015_auto_20150428_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='score',
        ),
    ]
