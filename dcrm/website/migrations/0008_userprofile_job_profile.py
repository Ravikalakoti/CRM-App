# Generated by Django 4.2.3 on 2023-08-03 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0007_message_is_read"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="job_profile",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]