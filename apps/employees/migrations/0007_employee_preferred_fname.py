# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-25 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20190623_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='preferred_fname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
