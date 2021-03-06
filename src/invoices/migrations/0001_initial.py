# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=127)),
                ('receiver', models.CharField(max_length=127)),
                ('notes', models.TextField()),
                ('terms', models.TextField()),
                ('date', models.DateField()),
                ('due_date', models.DateField()),
                ('payment_term', models.CharField(choices=[('UR', 'Upon Receipt'), ('N3', 'NET30'), ('N6', 'NET60')], default='UR', max_length=2)),
                ('discount_type', models.CharField(choices=[('$', 'Flat'), ('%', 'Percent')], default='%', max_length=1)),
                ('discount', models.IntegerField(default=0)),
                ('tax_type', models.CharField(choices=[('$', 'Flat'), ('%', 'Percent')], default='%', max_length=1)),
                ('tax', models.IntegerField(default=0)),
                ('shipping_price', models.IntegerField(default=0)),
                ('subtotal', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
