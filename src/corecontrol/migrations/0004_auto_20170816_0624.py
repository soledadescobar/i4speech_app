# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-16 06:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_keyword'),
        ('corecontrol', '0003_auto_20170520_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('consumer_key', models.CharField(max_length=100)),
                ('consumer_secret', models.CharField(max_length=100)),
                ('api_key', models.CharField(max_length=100)),
                ('api_secret', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidatos', models.ManyToManyField(to='control.Candidato')),
                ('keywords', models.ManyToManyField(to='control.Keyword')),
            ],
            options={
                'verbose_name': 'Configuracion',
                'verbose_name_plural': 'Configuraciones',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('ip', models.GenericIPAddressField()),
                ('apikey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecontrol.ApiKey')),
            ],
            options={
                'verbose_name': 'Servidor',
                'verbose_name_plural': 'Servidores',
            },
        ),
        migrations.CreateModel(
            name='ServerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo de Servidor',
                'verbose_name_plural': 'Tipos de Servidor',
            },
        ),
        migrations.AddField(
            model_name='server',
            name='server_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecontrol.ServerType'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecontrol.Server'),
        ),
    ]
