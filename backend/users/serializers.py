from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для восстановления пароля."""

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Проверка, существует ли пользователь с указанным email.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователя с таким email "
                                              "нет с системе.")
        return value
