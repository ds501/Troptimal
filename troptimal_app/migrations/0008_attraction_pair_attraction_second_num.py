# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0007_auto_20151205_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction_pair',
            name='attraction_second_num',
            field=models.PositiveIntegerField(null=True, default=0),
        ),
    ]
