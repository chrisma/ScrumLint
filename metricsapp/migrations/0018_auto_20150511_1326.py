# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0017_justintimedevelopment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='query',
            field=models.TextField(),
        ),
    ]
