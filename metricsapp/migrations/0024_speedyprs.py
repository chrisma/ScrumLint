# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0023_auto_20150604_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeedyPRs',
            fields=[
                ('sprintmetric_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='metricsapp.SprintMetric')),
            ],
            bases=('metricsapp.sprintmetric',),
        ),
    ]
