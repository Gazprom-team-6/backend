from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Skill

User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для восстановления пароля."""

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Проверка, существует ли пользователь с указанным email.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователя с таким email "
                "нет с системе."
            )
        return value


class SkillSerializer(serializers.Serializer):
    """Сериализатор для навыков сотрудника."""

    class Meta:
        model = Skill
        fields = ["name"]


class ProfileGetSerializer(serializers.Serializer):
    """Сериализатор для получения профиля пользователя."""

    skills = SkillSerializer(many=True)

    class Meta:
        model = User
        fields = ["employee_fio", "email", "employee_position",
                  "employee_date_of_birth", "employee_date_of_hire",
                  "employee_avatar", "employee_telegram", "employee_telephone",
                  "employee_type_job", "employee_status", "employee_location",
                  "employee_grade", "employee_description",
                  "is_employee_outsource", "skills", "employee_departament"]


class ProfileWriteSuperuserSerializer(serializers.Serializer):
    """
    Сериализатор для создания и изменения
    профиля сотрудника суперпользователем.
    """

    skills = SkillSerializer(many=True)

    class Meta:
        model = User
        fields = ["employee_fio", "email", "employee_position",
                  "employee_date_of_birth", "employee_date_of_hire",
                  "employee_avatar", "employee_telegram", "employee_telephone",
                  "employee_type_job", "employee_status", "employee_location",
                  "employee_grade", "employee_description", "is_superuser"
                  "is_employee_outsource", "skills", "employee_departament"]


class ProfilePatchUserSerializer(serializers.Serializer):
    """
    Сериализатор для изменения
    профиля сотрудника самим сотрудником.
    """

    class Meta:
        model = User
        fields = ["employee_telegram", "employee_telephone",
                  "employee_status", "employee_location", "skills",
                  "employee_description"]


class ProfileListSerializer(serializers.Serializer):
    """Сериализатор для получения списка сотрудников."""

    class Meta:
        model = User
        fields = ["employee_fio", "employee_avatar", "employee_position",
                  "employee_departament", "employee_telegram",
                  "employee_telephone", "email", "employee_type_job"]


class AvatarUploadSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аватара."""

    class Meta:
        model = User
        fields = ['employee_avatar']
