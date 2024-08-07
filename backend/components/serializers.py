from rest_framework import serializers

from components.models import Component


class ComponentBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для компонента."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Component
        fields = "__all__"


class ComponentReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения компонентов."""

    component_owner = serializers.StringRelatedField()
    component_second_owner = serializers.StringRelatedField()

    class Meta:
        model = Component
        fields = "__all__"


class ComponentReadShortSerializer(serializers.ModelSerializer):
    """Сериализатор для получения компонентов с ограниченным числом полей."""

    class Meta:
        model = Component
        fields = ["id", "component_name"]


class ComponentWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и изменения компонентов."""

    class Meta:
        model = Component
        fields = "__all__"

    def validate(self, attrs):
        """Проверяем, что заместитель и руководитель это разные люди."""
        component_owner = attrs.get("component_owner")
        component_second_owner = attrs.get("component_second_owner")
        if (component_owner and component_second_owner and
                component_second_owner == component_second_owner):
            raise serializers.ValidationError("Заместитель и руководитель "
                                              "не могут быть одним человеком")
        return attrs
