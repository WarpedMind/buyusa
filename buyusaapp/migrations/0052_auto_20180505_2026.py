# Generated by Django 2.0.2 on 2018-05-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyusaapp', '0051_auto_20180505_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C5', 'Category 5'), ('C3', 'Category 3'), ('C4', 'Category 4'), ('C2', 'Category 2'), ('C1', 'Category 1')], default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='importdata',
            name='ImportID',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyCategory',
            field=models.CharField(choices=[('b2b', 'Business-to-Business'), ('b2c', 'Business-to-Consumer')], default='b2c', max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyType',
            field=models.CharField(choices=[('retail', 'Retail'), ('manufacturer', 'Manufacturer'), ('service', 'Service'), ('wholesale', 'Wholesale'), ('independent', 'Independent')], default='manufacturer', max_length=12),
        ),
    ]
