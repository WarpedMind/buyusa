# Generated by Django 2.0.2 on 2018-09-24 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyusaapp', '0063_auto_20180923_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C4', 'Category 4'), ('C5', 'Category 5'), ('C1', 'Category 1'), ('C3', 'Category 3'), ('C2', 'Category 2')], default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyCategory',
            field=models.CharField(choices=[('b2b', 'Business-to-Business'), ('b2c', 'Business-to-Consumer')], default='b2c', max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyType',
            field=models.CharField(choices=[('retail', 'Retail'), ('service', 'Service'), ('manufacturer', 'Manufacturer'), ('independent', 'Independent'), ('wholesale', 'Wholesale')], default='manufacturer', max_length=12),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_updated',
            field=models.BooleanField(default=False),
        ),
    ]
