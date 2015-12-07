# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='attractions',
            fields=[
                ('attraction_number', models.PositiveIntegerField(serialize=False, default=0, primary_key=True)),
                ('attraction_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('attraction_city', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='attractions_pairs',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('attraction_pair', models.CharField(default='', max_length=30)),
                ('attraction', models.ForeignKey(default=None, to='troptimal_app.attractions')),
            ],
        ),
        migrations.CreateModel(
            name='output',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('attraction_pair', models.ForeignKey(to='troptimal_app.attractions_pairs')),
            ],
        ),
        migrations.CreateModel(
            name='trop_request',
            fields=[
                ('request_number', models.PositiveIntegerField(serialize=False, default=0, primary_key=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('attract_list_nums', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='output',
            name='user_trop_request',
            field=models.ForeignKey(to='troptimal_app.trop_request'),
        ),
        migrations.AddField(
            model_name='attractions_pairs',
            name='user_trop_request',
            field=models.ForeignKey(to='troptimal_app.trop_request'),
        ),
    ]
