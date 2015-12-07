# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attractions',
            name='attraction_country',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='attractions',
            name='attraction_state',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='attraction_city',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
