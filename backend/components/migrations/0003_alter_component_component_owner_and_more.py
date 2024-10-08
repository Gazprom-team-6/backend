# Generated by Django 4.2 on 2024-08-18 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("components", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="component",
            name="component_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owned_components",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Ответственный за компонент",
            ),
        ),
        migrations.AlterField(
            model_name="component",
            name="component_second_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="second_owned_components",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Заместитель ответственного за компонент",
            ),
        ),
    ]
