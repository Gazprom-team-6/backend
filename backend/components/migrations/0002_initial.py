# Generated by Django 4.2 on 2024-08-12 15:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("components", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="component",
            name="component_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="owned_components",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Ответственный за компонент",
            ),
        ),
        migrations.AddField(
            model_name="component",
            name="component_second_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="second_owned_components",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заместитель ответственного за компонент",
            ),
        ),
        migrations.AddIndex(
            model_name="component",
            index=models.Index(
                fields=["component_description"],
                name="components__compone_5bd1d7_idx"
            ),
        ),
    ]
