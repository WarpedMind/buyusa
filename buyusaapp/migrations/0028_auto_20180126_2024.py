# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-01-26 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyusaapp', '0027_auto_20180126_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='BrandCustomerServicePhone',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C4', 'Category 4'), ('C3', 'Category 3'), ('C1', 'Category 1'), ('C2', 'Category 2'), ('C5', 'Category 5')], max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyType',
            field=models.CharField(choices=[('service', 'Service'), ('retail', 'Retail'), ('independent', 'Independent'), ('wholesale', 'Wholesale'), ('manufacturer', 'Manufacturer')], default='manufacturer', max_length=12),
        ),
    ]