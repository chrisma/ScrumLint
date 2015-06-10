# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0026_monsterstories'),
    ]

    operations = [
        migrations.CreateModel(
            name='UntestedComplexity',
            fields=[
                ('sprintmetric_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='metricsapp.SprintMetric')),
            ],
            bases=('metricsapp.sprintmetric',),
        ),
        migrations.AlterField(
            model_name='metric',
            name='severity',
            field=models.FloatField(default=1.0, choices=[(1.5, 'High'), (1.0, 'Normal'), (0.5, 'Low')]),
        ),
    ]
