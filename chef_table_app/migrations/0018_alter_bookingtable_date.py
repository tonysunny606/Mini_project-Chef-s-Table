# Generated by Django 5.0.3 on 2024-11-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0017_complient_booking_complient_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingtable',
            name='Date',
            field=models.DateField(),
        ),
    ]