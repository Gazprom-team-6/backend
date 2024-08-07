from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from components.models import Component

User = get_user_model()


# Create your models here.
class Product(models.Model):
    """Модель продукта."""

    product_name = models.CharField(
        max_length=250,
        verbose_name="Название",
        unique=True
    )
    product_manager = models.ForeignKey(
        to=User,
        verbose_name="Менеджер продукта",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product_description = models.TextField(verbose_name="Описание продукта")
    parent_product = models.ForeignKey(
        to='self',
        verbose_name="Родительский продукт",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children_product'
    )
    component = models.ManyToManyField(
        to=Component,
        verbose_name="Компонент",
    )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        default_related_name = "product"

    def clean(self):
        """
        Проверяем, что родителем продукта не назначен сам продукт.
        """
        if self.parent_product == self:
            raise ValidationError("Product cannot be a parent to itself.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
