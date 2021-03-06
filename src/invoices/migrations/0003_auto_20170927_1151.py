# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_auto_20170927_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='discount_type',
            field=models.CharField(choices=[('$', '$'), ('%', '%')], default='%', max_length=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_type',
            field=models.CharField(choices=[('$', '$'), ('%', '%')], default='%', max_length=1),
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Invoice'),
        ),
    ]
