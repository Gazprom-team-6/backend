from django.contrib.auth.models import AbstractUser
from django.db import models

from company.models import Department
from users.constants import EMPLOYEE_STATUS, JOB_TYPES
from users.constants import GRADES
from users.validators import (phone_regex, validate_birth_date,
                              validate_hire_date)


class GazpromUser(AbstractUser):
    """Модель пользователя (сотрудника)."""

    employee_fio = models.CharField(max_length=250, verbose_name="ФИО")
    employee_position = models.CharField(
        verbose_name="Должность",
        max_length=250
    )
    employee_date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birth_date]
    )
    employee_date_of_hire = models.DateField(
        verbose_name="Дата найма",
        validators=[validate_hire_date]
    )
    employee_avatar = models.ImageField(verbose_name="Аватар")
    employee_telegram = models.CharField(
        verbose_name="Телеграм",
        unique=True,
        max_length=50,
    )
    employee_telephone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        unique=True,
        verbose_name="Номер телефона",
    )
    employee_type_job = models.CharField(
        verbose_name="Тип занятости",
        choices=JOB_TYPES,
        max_length=50,

    )
    employee_status = models.CharField(
        verbose_name="Статус",
        choices=EMPLOYEE_STATUS,
        max_length=50,
    )
    employee_location = models.CharField(
        verbose_name="Локация",
        max_length=300,
    )
    employee_grade = models.CharField(
        verbose_name="Грейд",
        choices=GRADES,
        max_length=50,
    )
    employee_description = models.TextField(verbose_name="Биография")
    is_employee_outsource = models.BooleanField(
        verbose_name="Outsource",
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Суперпользователь",
    )

    skills = models.ManyToManyField(
        to="Skill",
        verbose_name="Навыки"
    )
    employee_departament = models.ForeignKey(
        Department,
        verbose_name="Департамент",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
        default_related_name = "users"

    def __str__(self):
        return f"{self.employee_fio} / Департамент {self.employee_departament}"


class Skill(models.Model):
    """Модель навыков сотрудника."""

    name = models.CharField(
        verbose_name="Название",
        max_length=150,
        unique=True,
    )

    class Meta:
        verbose_name = "навык"
        verbose_name_plural = "Навыки"
        default_related_name = "skills"

    def __str__(self):
        return self.name
