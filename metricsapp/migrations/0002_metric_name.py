# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='name',
            field=models.CharField(default='Placeholdername', max_length=50),
            preserve_default=False,
        ),
    ]
