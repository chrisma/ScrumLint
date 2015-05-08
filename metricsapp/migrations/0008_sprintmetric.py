# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0007_auto_20150423_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='SprintMetric',
            fields=[
                ('metric_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='metricsapp.Metric')),
            ],
            bases=('metricsapp.metric',),
        ),
    ]
