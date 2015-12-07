# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0002_auto_20151204_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractions',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
