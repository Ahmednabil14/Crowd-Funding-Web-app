# Generated by Django 4.2.16 on 2024-09-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_rename_post_comment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='donations',
            field=models.JSONField(default=dict),
        ),
    ]
