# Generated by Django 2.0.2 on 2018-03-30 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyusaapp', '0047_auto_20180323_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='BrandCaption1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gig',
            name='BrandCaption2',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gig',
            name='BrandCaption3',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gig',
            name='BrandCaption4',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gig',
            name='BrandCaption5',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='gig',
            name='BrandCaption6',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C4', 'Category 4'), ('C1', 'Category 1'), ('C2', 'Category 2'), ('C5', 'Category 5'), ('C3', 'Category 3')], default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyCategory',
            field=models.CharField(choices=[('b2c', 'Business-to-Consumer'), ('b2b', 'Business-to-Business')], default='b2c', max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyType',
            field=models.CharField(choices=[('independent', 'Independent'), ('service', 'Service'), ('retail', 'Retail'), ('manufacturer', 'Manufacturer'), ('wholesale', 'Wholesale')], default='manufacturer', max_length=12),
        ),
    ]