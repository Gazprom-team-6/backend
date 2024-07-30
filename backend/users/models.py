from backend.users.constants import EMPLOYEE_STATUS, JOB_TYPES
from backend.users.validators import phone_regex, validate_birth_date
from django.contrib.auth.models import AbstractUser
from django.db import models


class GazpromUser(AbstractUser):
    """Модель пользователя."""

    employee_fio = models.CharField(max_length=250, verbose_name="ФИО")
    employee_position = models.CharField(
        verbose_name="Должность",
        max_length=250
    )
    employee_date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birth_date]
    )
    employee_avatar = models.ImageField(verbose_name="Аватар")
    employee_telegram = models.CharField(
        verbose_name="Телеграм",
        max_length=50
    )
    employee_telephone = models.CharField(
        validators=[phone_regex], max_length=20, unique=True,
        verbose_name="Номер телефона"
    )
    employee_type_job = models.CharField(
        verbose_name="Тип занятости",
        choices=JOB_TYPES,
        max_length=50

    )
    employee_status = models.CharField(
        verbose_name="Статус",
        choices=EMPLOYEE_STATUS,
        max_length=50
    )
    employee_location = models.CharField(
        verbose_name="Локация",
        max_length=300
    )
    employee_grade = models.CharField(
        verbose_name="Грейд",
        max_length=50
    )
    employee_description = models.TextField(verbose_name="Биография")
    employee_outsource = models.BooleanField(verbose_name="Outsource")
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Суперпользователь"
    )


class Skill(models.Model):
    """Навыки сотрудников."""
