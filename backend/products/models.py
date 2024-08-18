from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from components.models import Component

User = get_user_model()


class Product(models.Model):
    """Модель продукта."""

    product_name = models.CharField(
        max_length=250, verbose_name="Название", unique=True
    )
    product_manager = models.ForeignKey(
        to=User,
        verbose_name="Менеджер продукта",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    product_description = models.TextField(verbose_name="Описание продукта")
    parent_product = models.ForeignKey(
        to="self",
        verbose_name="Родительский продукт",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children_product",
    )
    components = models.ManyToManyField(
        to=Component,
        through="ProductComponent",
        verbose_name="Компонент",
        blank=True
    )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        default_related_name = "product"
        indexes = [
            models.Index(fields=["product_description"]),
        ]

    def __str__(self):
        return self.product_name

    def clean(self):
        """
        Проверяем, что родителем продукта не назначен сам продукт.
        """
        if self.parent_product == self:
            raise ValidationError("Product cannot be a parent to itself.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProductComponent(models.Model):
    """Промежуточная модель для связи продуктов и компонентов."""

    product = models.ForeignKey(
        to=Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
    )
    component = models.ForeignKey(
        to=Component,
        verbose_name="Компонент",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "component"],
                name="unique_product_component"
            )
        ]
        verbose_name = "компонент продукта"
        verbose_name_plural = "Компоненты продуктов"
        default_related_name = "productcomponent"
