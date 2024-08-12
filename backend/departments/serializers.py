from rest_framework import serializers

from company.serializers import AddEmployeesBaseSerializer
from departments.models import Department
from users.serializers import EmployeeShortGetSerializer


class DepartmentBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для департаментов."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner"]


class DepartmentWriteSerializer(DepartmentBaseSerializer):
    """Сериализатор для создания и изменения департаментов."""

    class Meta:
        model = Department
        fields = "__all__"

    def validate_parent_department(self, value):
        """
        Проверяем, что родителем департамента не назначен сам департамент.
        """
        if self.instance and value == self.instance:
            raise serializers.ValidationError(
                "Нельзя назначить родительским "
                "департаментом сам департамент."
            )
        return value


class DepartmentReadSerializer(DepartmentBaseSerializer):
    """Сериализатор для получения департаментов."""

    departament_owner = EmployeeShortGetSerializer()
    parent_department = DepartmentBaseSerializer()
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner",
                  "departament_description", "parent_department",
                  "employee_count"]


class DepartmentChildrenReadSerializer(DepartmentBaseSerializer):
    """Сериализатор для получения дочерних департаментов."""

    departament_owner = EmployeeShortGetSerializer()
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner",
                  "departament_description", "employee_count"]


class DepartmentAddEmployeesSerializer(AddEmployeesBaseSerializer):
    """Сериализатор для добавления сотрудников в департамент."""
