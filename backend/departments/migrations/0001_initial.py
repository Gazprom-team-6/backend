# Generated by Django 4.2 on 2024-08-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "departament_name",
                    models.CharField(
                        max_length=250, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "departament_description",
                    models.TextField(verbose_name="Описание отдела"),
                ),
            ],
            options={
                "verbose_name": "департамент",
                "verbose_name_plural": "Департаменты",
                "default_related_name": "departament",
            },
        ),
    ]
