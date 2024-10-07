# Generated by Django 5.0.3 on 2024-10-01 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0006_events'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingtable',
            old_name='Quantity',
            new_name='mealstype',
        ),
        migrations.RemoveField(
            model_name='bookingtable',
            name='SHEDULE',
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='ChefTable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.cheftable'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='number_gas',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='serving_time',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]