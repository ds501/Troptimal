# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0005_auto_20151205_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='attractions_pairs',
            name='duration',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='attractions_pairs',
            name='value',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='trop_request',
            name='finish_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='trop_request',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='address',
            field=models.CharField(default='', null=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='description',
            field=models.CharField(default='', null=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='trop_request',
            name='attract_list_nums',
            field=models.CharField(default='', null=True, max_length=50),
        ),
    ]
