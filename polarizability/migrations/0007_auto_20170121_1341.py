# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polarizability', '0006_delete_lab_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crystals',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
