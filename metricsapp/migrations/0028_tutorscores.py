# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0027_auto_20150610_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorScores',
            fields=[
                ('sprintmetric_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='metricsapp.SprintMetric')),
            ],
            bases=('metricsapp.sprintmetric',),
        ),
    ]
