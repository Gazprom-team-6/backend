from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
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
        to="products.Product",
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

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для добавления team_manager
        в GazpromUserTeam с ролью 'Руководитель'.
        """
        super().save(*args, **kwargs)  # Сначала сохраняем команду

        if self.team_manager:
            # Проверяем, если уже есть запись для этого менеджера в этой
            # команде
            gazprom_user_team, created = GazpromUserTeam.objects.get_or_create(
                employee=self.team_manager,
                team=self,
                defaults={'role': 'Руководитель'}
            )
            if not created:
                # Если запись существует, обновляем роль
                gazprom_user_team.role = 'Руководитель'
                gazprom_user_team.save()


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
                fields=['employee', 'team'],
                name='one_employee_role_in_one_team'
            )
        ]

    def __str__(self):
        return (f"{self.team.team_name} – {self.employee.employee_fio} – "
                f"{self.role}")
