# Generated by Django 4.2.16 on 2024-09-12 20:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='users/images')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('facebook_profile', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=30, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
