# Generated by Django 4.2.3 on 2023-08-03 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0010_alter_education_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="education",
            name="field_of_study",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
