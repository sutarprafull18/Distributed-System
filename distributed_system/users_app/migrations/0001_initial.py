# Generated by Django 4.2.17 on 2025-01-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
            ],
            options={
                'db_table': 'users_app_user',
            },
        ),
    ]
