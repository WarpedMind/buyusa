# Generated by Django 2.0.2 on 2018-08-15 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyusaapp', '0058_auto_20180814_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C2', 'Category 2'), ('C3', 'Category 3'), ('C4', 'Category 4'), ('C5', 'Category 5'), ('C1', 'Category 1')], default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='profile',
            name='CompanyType',
            field=models.CharField(choices=[('service', 'Service'), ('manufacturer', 'Manufacturer'), ('retail', 'Retail'), ('wholesale', 'Wholesale'), ('independent', 'Independent')], default='manufacturer', max_length=12),
        ),
    ]