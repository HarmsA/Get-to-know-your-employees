# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-22 16:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='how_well_known',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='how_well_known',
            name='user',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='How_well_known',
        ),
    ]
