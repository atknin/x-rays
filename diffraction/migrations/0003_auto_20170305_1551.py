# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-05 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diffraction', '0002_auto_20170305_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_of_calcs',
            name='PC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diffraction.PC'),
        ),
    ]
