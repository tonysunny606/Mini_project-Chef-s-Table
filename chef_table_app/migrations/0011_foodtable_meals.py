# Generated by Django 5.0.3 on 2024-10-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0010_foodtable_cuisine_foodtable_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtable',
            name='Meals',
            field=models.CharField(default='qwer', max_length=50),
            preserve_default=False,
        ),
    ]
