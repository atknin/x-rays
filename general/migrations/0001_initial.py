# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='updates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('what_is', models.CharField(max_length=300)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'кристалл',
                'verbose_name_plural': 'кристаллы',
                'ordering': ['-date'],
            },
        ),
    ]
