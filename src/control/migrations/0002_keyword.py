# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-16 04:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Keyword o Hashtag comenzando con #', max_length=100, verbose_name='Keyword')),
            ],
        ),
    ]
