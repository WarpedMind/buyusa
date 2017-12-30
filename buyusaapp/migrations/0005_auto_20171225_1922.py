# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-12-25 19:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyusaapp', '0004_auto_20171223_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.CharField(choices=[('C5', 'Category 5'), ('C3', 'Category 3'), ('C4', 'Category 4'), ('C2', 'Category 2'), ('C1', 'Category 1')], max_length=2),
        ),
        migrations.AddField(
            model_name='purchase',
            name='gig',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyusaapp.Gig'),
        ),
    ]