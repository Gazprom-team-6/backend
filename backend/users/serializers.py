from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.constants import EMPLOYEE_STATUS, GRADES, JOB_TYPES
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


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для навыков сотрудника."""

    class Meta:
        model = Skill
        fields = ["name"]


class EmployeeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения профиля пользователя."""

    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["id", "employee_fio", "email", "employee_position",
                  "employee_date_of_birth", "employee_date_of_hire",
                  "employee_avatar", "employee_telegram", "employee_telephone",
                  "employee_type_job", "employee_status", "employee_location",
                  "employee_grade", "employee_description",
                  "is_employee_outsource", "skills", "employee_departament"]


class EmployeeWriteSuperuserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и изменения
    профиля сотрудника суперпользователем.
    """

    password = serializers.CharField(max_length=128, write_only=True)
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        required=False
    )
    employee_date_of_hire = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )
    employee_date_of_birth = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )
    employee_type_job = serializers.ChoiceField(
        choices=JOB_TYPES,
        required=False
    )
    employee_status = serializers.ChoiceField(
        choices=EMPLOYEE_STATUS,
        required=False
    )
    employee_grade = serializers.ChoiceField(choices=GRADES, required=False)
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "password", "employee_fio", "email",
                  "employee_position",
                  "employee_date_of_birth", "employee_date_of_hire",
                  "employee_telegram", "employee_telephone",
                  "employee_type_job", "employee_status", "employee_location",
                  "employee_grade", "employee_description", "is_superuser",
                  "is_employee_outsource", "skills", "employee_departament"]

    def create(self, validated_data):
        """Создание пользователя."""
        # Шифруем пароль
        validated_data["password"] = make_password(
            validated_data.get("password")
        )
        return super(EmployeeWriteSuperuserSerializer, self).create(
            validated_data
        )


class EmployeePatchUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения
    профиля сотрудника самим сотрудником.
    """

    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True
    )
    employee_status = serializers.ChoiceField(choices=EMPLOYEE_STATUS)
    id = serializers.ReadOnlyField()
    is_superuser = serializers.HiddenField

    class Meta:
        model = User
        fields = ["id", "employee_telegram", "employee_telephone",
                  "employee_status", "employee_location", "skills",
                  "employee_description", "is_superuser"]


class EmployeeListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка сотрудников."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "employee_fio", "employee_avatar", "employee_position",
                  "employee_departament", "employee_telegram",
                  "employee_telephone", "email", "employee_type_job", "employee_grade"]


class EmployeeShortGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения укороченного списка данных профиля
    сотрудника.
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "employee_fio", "employee_avatar", "employee_position",
                  "employee_grade"]


class EmployeeIdFIOGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения ID и ФИО сотрудника.
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "employee_fio"]


class AvatarUploadSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки аватара."""

    employee_avatar = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=True
    )

    class Meta:
        model = User
        fields = ["employee_avatar"]
