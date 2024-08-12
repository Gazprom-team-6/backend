from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from users.constants import EMPLOYEE_STATUS, GRADES, JOB_TYPES
from users.manager import GazpromUserManager
from users.validators import (phone_regex, validate_birth_date,
                              validate_hire_date)


class GazpromUser(AbstractUser):
    """Модель пользователя (сотрудника)."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = GazpromUserManager()

    employee_fio = models.CharField(
        max_length=250,
        verbose_name="ФИО",
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="Адрес электронной почты",
    )
    employee_position = models.CharField(
        verbose_name="Должность",
        max_length=250,
        null=True,
        blank=True,
    )
    employee_date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birth_date],
        null=True,
        blank=True
    )
    employee_date_of_hire = models.DateField(
        verbose_name="Дата найма",
        validators=[validate_hire_date],
        null=True,
        blank=True
    )
    employee_avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to='avatars/',
        null=True,
        blank=True
    )
    employee_telegram = models.CharField(
        verbose_name="Телеграм",
        max_length=50,
        null=True,
        blank=True,
    )
    employee_telephone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        verbose_name="Номер телефона",
        null=True,
        blank=True,
    )
    employee_type_job = models.CharField(
        verbose_name="Тип занятости",
        choices=JOB_TYPES,
        max_length=50,
        null=True,
        blank=True
    )
    employee_status = models.CharField(
        verbose_name="Статус",
        choices=EMPLOYEE_STATUS,
        max_length=50,
        null=True,
        blank=True
    )
    employee_location = models.CharField(
        verbose_name="Локация",
        max_length=300,
        null=True,
        blank=True
    )
    employee_grade = models.CharField(
        verbose_name="Грейд",
        choices=GRADES,
        max_length=50,
        null=True,
        blank=True
    )
    employee_description = models.TextField(
        verbose_name="Биография",
        null=True,
        blank=True
    )
    is_employee_outsource = models.BooleanField(
        verbose_name="Outsource",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="Суперпользователь",
        default=False,
    )
    skills = models.ManyToManyField(
        to="Skill",
        through="EmployeeSkill",
        verbose_name="Навыки",
        blank=True
    )
    employee_departament = models.ForeignKey(
        to="departments.Department",
        verbose_name="Департамент",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    username = None

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
        default_related_name = "users"
        indexes = [
            models.Index(fields=["employee_fio"]),
            models.Index(fields=["employee_position"]),
            models.Index(fields=["employee_telegram"]),
            models.Index(fields=["employee_telephone"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['employee_telegram'],
                name='unique_employee_telegram',
                condition=~Q(employee_telegram=None),
            ),
            models.UniqueConstraint(
                fields=['employee_telephone'],
                name='unique_employee_telephone',
                condition=~Q(employee_telephone=None),
            ),
        ]

    def __str__(self):
        return f"{self.employee_fio}"


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


class EmployeeSkill(models.Model):
    """Промежуточная модель для связи сотрудника и навыков."""

    employee = models.ForeignKey(
        to=GazpromUser,
        verbose_name="Сотрудник",
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        to=Skill,
        verbose_name="Навык",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'skill'],
                name='unique_employee_skill'
            )
        ]
        verbose_name = "навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        default_related_name = "employeeskill"
