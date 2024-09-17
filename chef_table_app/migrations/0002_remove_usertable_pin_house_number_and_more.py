# Generated by Django 5.0.3 on 2024-09-08 04:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef_table_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertable',
            name='pin_house_number',
        ),
        migrations.RemoveField(
            model_name='usertable',
            name='post_landmark',
        ),
        migrations.AddField(
            model_name='usertable',
            name='house_number',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertable',
            name='landmark',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertable',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertable',
            name='gender',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='phone',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ChefTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=50)),
                ('Qualification', models.CharField(max_length=50)),
                ('Experience', models.CharField(max_length=20)),
                ('phone', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chef_table_app.login_table')),
            ],
        ),
    ]
