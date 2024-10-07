# Generated by Django 5.0.3 on 2024-10-01 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0011_foodtable_meals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingtable',
            name='mealstype',
        ),
        migrations.RemoveField(
            model_name='bookingtable',
            name='serving_time',
        ),
        migrations.CreateModel(
            name='BookingTable1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mealstype', models.CharField(max_length=50)),
                ('serving_time', models.CharField(max_length=50)),
                ('BOOKING', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.bookingtable')),
            ],
        ),
    ]