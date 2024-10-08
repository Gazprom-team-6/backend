# Generated by Django 4.2 on 2024-08-18 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="parent_product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children_product",
                to="products.product",
                verbose_name="Родительский продукт",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Менеджер продукта",
            ),
        ),
    ]
