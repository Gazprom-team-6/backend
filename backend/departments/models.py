from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


# Create your models here.
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
        related_name='children_departament'
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

        # После сохранения проверяем, назначен ли руководитель
        if self.departament_owner:
            # Обновляем поле employee_departament у назначенного руководителя
            self.departament_owner.employee_departament = self
            self.departament_owner.save()
