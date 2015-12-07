# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0003_auto_20151204_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractions',
            name='address',
            field=models.CharField(max_length=500, default=None),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='attraction_name',
            field=models.CharField(max_length=100, default=None),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='description',
            field=models.CharField(max_length=500, default=None),
        ),
    ]
