from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Department(models.Model):
    """Модель департамента (отдела)."""

    departament_name = models.CharField(
        max_length=250,
        verbose_name="Название"
    )
    departament_owner = models.ForeignKey(
        to=User,
        verbose_name="Руководитель департамента",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    departament_description = models.TextField(verbose_name="Описание отдела")
    parent_department = models.ForeignKey(
        to='self',
        verbose_name="Родительский департамент",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "департамент"
        verbose_name_plural = "Департаменты"
        default_related_name = "departament"

    def __str__(self):
        return self.departament_name


class Team(models.Model):
    """Модель команды."""

    team_name = models.CharField(
        max_length=250,
        verbose_name="Название"
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



class Product(models.Model):
    """Модель продукта."""

    product_name = models.CharField(
        max_length=250,
        verbose_name="Название"
    )
    product_manager = models.ForeignKey(
        User,
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
