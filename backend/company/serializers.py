from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Department
from users.serializers import ProfileShortGetSerializer

User = get_user_model()


class DepartmentBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для департаментов."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner"]


class DepartmentWriteSerializer(DepartmentBaseSerializer):
    """Сериализатор для создания и изменения департаментов."""

    departament_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True
    )
    parent_department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True
    )

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

    departament_owner = ProfileShortGetSerializer()
    parent_department = DepartmentBaseSerializer()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner",
                  "departament_description", "parent_department"]
