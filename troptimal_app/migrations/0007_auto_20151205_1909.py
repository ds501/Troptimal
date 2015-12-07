# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troptimal_app', '0006_auto_20151205_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='attraction',
            fields=[
                ('attraction_number', models.PositiveIntegerField(primary_key=True, default=0, serialize=False)),
                ('attraction_name', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', null=True, max_length=500)),
                ('attraction_city', models.CharField(default='', max_length=100)),
                ('attraction_state', models.CharField(default='', max_length=100)),
                ('attraction_country', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', null=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='attraction_pair',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('attraction_pair', models.CharField(default='', max_length=30)),
                ('duration', models.PositiveIntegerField(null=True, default=0)),
                ('value', models.FloatField(null=True, default=0)),
                ('attraction', models.ForeignKey(default=None, to='troptimal_app.attraction')),
                ('user_trop_request', models.ForeignKey(to='troptimal_app.trop_request')),
            ],
        ),
        migrations.RemoveField(
            model_name='attractions_pairs',
            name='attraction',
        ),
        migrations.RemoveField(
            model_name='attractions_pairs',
            name='user_trop_request',
        ),
        migrations.AlterField(
            model_name='output',
            name='attraction_pair',
            field=models.ForeignKey(to='troptimal_app.attraction_pair'),
        ),
        migrations.DeleteModel(
            name='attractions',
        ),
        migrations.DeleteModel(
            name='attractions_pairs',
        ),
    ]
