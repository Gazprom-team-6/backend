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
        User,
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
