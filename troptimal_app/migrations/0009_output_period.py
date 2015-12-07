# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0008_attraction_pair_attraction_second_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='period',
            field=models.PositiveIntegerField(default=1000, null=True),
        ),
    ]
