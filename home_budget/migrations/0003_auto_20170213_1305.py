# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_budget', '0002_auto_20170209_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]