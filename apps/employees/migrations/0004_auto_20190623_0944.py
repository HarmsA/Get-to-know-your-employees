# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-23 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20190623_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, upload_to='quiz/media/'),
        ),
    ]
