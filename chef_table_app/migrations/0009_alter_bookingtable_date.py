# Generated by Django 5.0.3 on 2024-10-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0008_rename_cheftable_bookingtable_chef'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingtable',
            name='Date',
            field=models.CharField(max_length=50),
        ),
    ]