from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Component(models.Model):
    """Модель компонента."""

    component_name = models.CharField(
        max_length=250,
        verbose_name="Название",
        unique=True,
    )
    component_type = models.CharField(max_length=150, verbose_name="Тип")
    component_link = models.URLField(
        verbose_name="Ссылка на документацию", null=True, blank=True
    )
    component_owner = models.ForeignKey(
        to=User,
        verbose_name="Ответственный за компонент",
        related_name="owned_components",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    component_second_owner = models.ForeignKey(
        to=User,
        verbose_name="Заместитель ответственного за компонент",
        related_name="second_owned_components",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    component_description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "компонент"
        verbose_name_plural = "Компоненты"
        default_related_name = "component"
        indexes = [
            models.Index(fields=["component_description"]),
        ]

    def __str__(self):
        return self.component_name
