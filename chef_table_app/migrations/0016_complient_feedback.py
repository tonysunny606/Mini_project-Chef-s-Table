# Generated by Django 5.0.3 on 2024-10-24 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0015_bookingdetailstable_count_bookingdetailstable_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Complient', models.CharField(max_length=100)),
                ('date_submitted', models.DateField(auto_now_add=True)),
                ('date_replied', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Feedback', models.CharField(max_length=100)),
                ('rating', models.FloatField(default=0.0)),
                ('date', models.DateField(auto_now_add=True)),
                ('BOOKING', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.bookingtable')),
            ],
        ),
    ]
