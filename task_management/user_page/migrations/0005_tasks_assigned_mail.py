# Generated by Django 4.2 on 2023-05-29 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0004_tasks_assigned_to_tasks_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='assigned_mail',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
