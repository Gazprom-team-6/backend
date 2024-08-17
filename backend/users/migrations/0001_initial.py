# Generated by Django 4.2 on 2024-08-12 15:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("departments", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="GazpromUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("employee_fio", models.CharField(max_length=250, verbose_name="ФИО")),
                (
                    "email",
                    models.EmailField(
                        max_length=100,
                        unique=True,
                        verbose_name="Адрес электронной почты",
                    ),
                ),
                (
                    "employee_position",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Должность"
                    ),
                ),
                (
                    "employee_date_of_birth",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[users.validators.validate_birth_date],
                        verbose_name="Дата рождения",
                    ),
                ),
                (
                    "employee_date_of_hire",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[users.validators.validate_hire_date],
                        verbose_name="Дата найма",
                    ),
                ),
                (
                    "employee_avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="avatars/",
                        verbose_name="Аватар",
                    ),
                ),
                (
                    "employee_telegram",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Телеграм"
                    ),
                ),
                (
                    "employee_telephone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Номер телефона должен начинаться с + и состоять из 10-15 цифр",
                                regex="^\\+\\d{10,15}$",
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "employee_type_job",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("full_time", "полная занятость"),
                            ("part_time", "частичная занятость"),
                            ("internship", "стажировка"),
                        ],
                        max_length=50,
                        null=True,
                        verbose_name="Тип занятости",
                    ),
                ),
                (
                    "employee_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("working", "в работе"),
                            ("vacation", "отпуск"),
                            ("sick", "больничный"),
                            ("fired", "уволен"),
                        ],
                        max_length=50,
                        null=True,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "employee_location",
                    models.CharField(
                        blank=True, max_length=300, null=True, verbose_name="Локация"
                    ),
                ),
                (
                    "employee_grade",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "Gr-1"),
                            ("2", "Gr-2"),
                            ("3", "Gr-3"),
                            ("4", "Gr-4"),
                            ("5", "Gr-5"),
                            ("6", "Gr-6"),
                            ("7", "Gr-7"),
                        ],
                        max_length=50,
                        null=True,
                        verbose_name="Грейд",
                    ),
                ),
                (
                    "employee_description",
                    models.TextField(blank=True, null=True, verbose_name="Биография"),
                ),
                (
                    "is_employee_outsource",
                    models.BooleanField(default=False, verbose_name="Outsource"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False, verbose_name="Суперпользователь"
                    ),
                ),
                (
                    "employee_departament",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="departments.department",
                        verbose_name="Департамент",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "Пользователи",
                "default_related_name": "users",
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "навык",
                "verbose_name_plural": "Навыки",
                "default_related_name": "skills",
            },
        ),
        migrations.CreateModel(
            name="EmployeeSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Сотрудник",
                    ),
                ),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.skill",
                        verbose_name="Навык",
                    ),
                ),
            ],
            options={
                "verbose_name": "навык сотрудника",
                "verbose_name_plural": "Навыки сотрудников",
                "default_related_name": "employeeskill",
            },
        ),
        migrations.AddField(
            model_name="gazpromuser",
            name="skills",
            field=models.ManyToManyField(
                blank=True,
                through="users.EmployeeSkill",
                to="users.skill",
                verbose_name="Навыки",
            ),
        ),
        migrations.AddField(
            model_name="gazpromuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddConstraint(
            model_name="employeeskill",
            constraint=models.UniqueConstraint(
                fields=("employee", "skill"), name="unique_employee_skill"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_fio"], name="users_gazpr_employe_d53b37_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_position"], name="users_gazpr_employe_102259_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_telegram"], name="users_gazpr_employe_c82d51_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_telephone"], name="users_gazpr_employe_e796c8_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_grade"], name="users_gazpr_employe_64f9d1_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="gazpromuser",
            index=models.Index(
                fields=["employee_location"], name="users_gazpr_employe_3ad0bb_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="gazpromuser",
            constraint=models.UniqueConstraint(
                condition=models.Q(("employee_telegram", None), _negated=True),
                fields=("employee_telegram",),
                name="unique_employee_telegram",
            ),
        ),
        migrations.AddConstraint(
            model_name="gazpromuser",
            constraint=models.UniqueConstraint(
                condition=models.Q(("employee_telephone", None), _negated=True),
                fields=("employee_telephone",),
                name="unique_employee_telephone",
            ),
        ),
    ]
