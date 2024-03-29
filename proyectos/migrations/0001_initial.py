# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-10 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Ejecutando', 'Ejecutando'), ('Cancelado', 'Cancelado'), ('Finalizado', 'Finalizado')], max_length=50)),
                ('scrum_master', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto_User_Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(default='', max_length=100)),
                ('proyecto', models.CharField(default='', max_length=100)),
                ('rol', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
