from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AddEmployeesBaseSerializer(serializers.Serializer):
    """Базовый сериализатор для добавления сотрудников."""

    employee_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
    )

    def validate_employee_ids(self, value):
        """Проверяем, что сотрудники с переданными ID существуют в БД."""
        existing_ids = set(
            User.objects.filter(id__in=value).values_list(
                'id',
                flat=True
            )
        )
        provided_ids = set(value)
        # Получаем id сотрудников, которых не существует в БД
        missing_ids = provided_ids - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f"Следующие сотрудники не существуют: {list(missing_ids)}"
            )
        # Возвращаем список id без дубликатов
        return list(provided_ids)
