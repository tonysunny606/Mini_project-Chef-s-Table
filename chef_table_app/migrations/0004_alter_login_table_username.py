# Generated by Django 5.0.3 on 2024-09-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0003_cheftable_image_usertable_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_table',
            name='username',
            field=models.CharField(max_length=220),
        ),
    ]
