# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0022_metric_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitsPerDev',
            fields=[
                ('sprintmetric_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='metricsapp.SprintMetric')),
            ],
            bases=('metricsapp.sprintmetric',),
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'categories'},
        ),
    ]
