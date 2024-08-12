from rest_framework import serializers

from company.serializers import AddEmployeesBaseSerializer
from products.serializers import (ProductBaseSerializer,
                                  ProductShortReadSerializer)
from teams.models import GazpromUserTeam, Team
from users.serializers import (EmployeeIdFIOGetSerializer,
                               EmployeeShortGetSerializer)


class TeamBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для команд."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Team
        fields = "__all__"


class TeamWriteSerializer(TeamBaseSerializer):
    """Сериализатор для добавления и изменения команд."""

    class Meta:
        model = Team
        fields = "__all__"


class TeamListSerializer(TeamBaseSerializer):
    """Сериализатор для получения списка команд."""

    team_manager = EmployeeShortGetSerializer()
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ["id", "team_name", "team_manager", "product",
                  "employee_count"]


class TeamGetSerializer(TeamBaseSerializer):
    """Сериализатор для получения информации о команде."""

    team_manager = EmployeeShortGetSerializer()
    product = ProductShortReadSerializer()
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ["id", "team_name", "team_manager", "product",
                  "employee_count"]


class TeamAddEmployeesSerializer(AddEmployeesBaseSerializer):
    """Сериализатор для добавления сотрудников в команду."""

    role = serializers.CharField(max_length=100, min_length=3)

    def validate(self, attrs):
        """
        Проверяем, есть ли переданные сотрудники уже в команде.
        """
        employee_ids = attrs['employee_ids']
        team = self.context['team']

        # Получаем список id сотрудников, которые уже есть в команде
        already_in_team = GazpromUserTeam.objects.filter(
            employee_id__in=employee_ids,
            team=team,
        ).select_related("employee").values_list(
            'employee__employee_fio',
            flat=True
        )
        # Если такие сотрудники есть, то возвращаем ошибку и список ФИО
        # сотрудников
        if already_in_team:
            raise serializers.ValidationError(
                f"Следующие сотрудники уже в команде: "
                f"{', '.join(already_in_team)}"
            )

        return attrs


class TeamDeleteEmployeesSerializer(AddEmployeesBaseSerializer):
    """Сериализатор для удаления сотрудников из команды."""


class TeamEmployeeListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка сотрудников команды."""

    employee = EmployeeShortGetSerializer()

    class Meta:
        model = GazpromUserTeam
        fields = ["role", "employee"]
