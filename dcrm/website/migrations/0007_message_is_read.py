# Generated by Django 4.2.3 on 2023-08-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
    ]