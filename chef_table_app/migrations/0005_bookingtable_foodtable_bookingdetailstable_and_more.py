# Generated by Django 5.0.3 on 2024-09-17 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0004_alter_login_table_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.CharField(max_length=50)),
                ('Status', models.CharField(max_length=50)),
                ('Date', models.DateField()),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.usertable')),
            ],
        ),
        migrations.CreateModel(
            name='FoodTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('Details', models.CharField(max_length=50)),
                ('Price', models.CharField(max_length=50)),
                ('Date', models.DateField()),
                ('CHEF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.cheftable')),
            ],
        ),
        migrations.CreateModel(
            name='BookingDetailsTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BOOKING', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.bookingtable')),
                ('FOOD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.foodtable')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_time', models.CharField(max_length=50)),
                ('To_time', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('CHEF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.cheftable')),
            ],
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='SHEDULE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.scheduletable'),
        ),
    ]
