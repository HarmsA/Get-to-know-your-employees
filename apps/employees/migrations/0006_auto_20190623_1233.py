# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-23 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_auto_20190623_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_image',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='employees.Employee'),
        ),
    ]
