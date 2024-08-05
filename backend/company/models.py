from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Department(models.Model):
    """Модель департамента (отдела)."""

    departament_name = models.CharField(
        max_length=250,
        verbose_name="Название",
        unique=True
    )
    departament_description = models.TextField(verbose_name="Описание отдела")
    departament_owner = models.ForeignKey(
        to=User,
        verbose_name="Руководитель департамента",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    parent_department = models.ForeignKey(
        to='self',
        verbose_name="Родительский департамент",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "департамент"
        verbose_name_plural = "Департаменты"
        default_related_name = "departament"

    def __str__(self):
        return self.departament_name

    def clean(self):
        """
        Проверяем, что родителем департамента не назначен сам департамент.
        """
        if self.parent_department == self:
            raise ValidationError("Department cannot be a parent to itself.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Team(models.Model):
    """Модель команды."""

    team_name = models.CharField(
        max_length=250,
        verbose_name="Название",
        unique=True
    )
    team_manager = models.ForeignKey(
        to=User,
        verbose_name="Менеджер команды",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        to="Product",
        verbose_name="Родительский продукт",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "команда"
        verbose_name_plural = "Команды"
        default_related_name = "team"

    def __str__(self):
        return self.team_name


class GazpromUserTeam(models.Model):
    """Модель для связи сотрудников и команд."""

    employee = models.ForeignKey(
        to=User,
        verbose_name="Сотрудник", on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        to=Team,
        verbose_name="Команда",
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        verbose_name="Роль сотрудника в команде",
        max_length=100
    )

    class Meta:
        verbose_name = "роль сотрудника в команде"
        verbose_name_plural = "Роли сотрудников в командах"
        default_related_name = "gazpromuserteam"
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'team', 'role'],
                name='Unique employee role in team'
            )
        ]


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


class Component(models.Model):
    """Модель компонента."""

    component_name = models.CharField(
        max_length=250,
        verbose_name="Название",
        unique=True
    )
    component_type = models.CharField(
        max_length=150,
        verbose_name="Тип"
    )
    component_link = models.URLField(
        verbose_name="Ссылка на документацию",
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
    component_description = models.TextField(
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "компонент"
        verbose_name_plural = "Компоненты"
        default_related_name = "component"

    def __str__(self):
        return self.component_name


class AdditionalField(models.Model):
    """Модель для дополнительных полей."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Содержание поля")

    class Meta:
        verbose_name = "компонент"
        verbose_name_plural = "Компоненты"
        default_related_name = "component"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.name


class Metric(models.Model):
    """Модель метрик."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Содержание метрики")

    class Meta:
        verbose_name = "метрика"
        verbose_name_plural = "Метрики"
        default_related_name = "metric"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.name
