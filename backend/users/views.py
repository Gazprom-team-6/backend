from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, parsers, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.mixins import BaseViewSet
from users.filters import GazpromUserFilter
from users.permissions import IsSuperuser, IsSuperuserOrProfileOwner
from users.schemas import (DELETE_AVATAR_SCHEMA, GAZPROMUSER_SCHEMA, ME_SCHEMA,
                           PASSWORD_RESET_VIEW_SCHEMA, UPLOAD_AVATAR_SCHEMA)
from users.serializers import (AvatarUploadSerializer, EmployeeGetSerializer,
                               EmployeeListSerializer,
                               EmployeePatchUserSerializer,
                               EmployeeWriteSuperuserSerializer,
                               PasswordResetSerializer)
from users.tasks import send_reset_password_email

User = get_user_model()


@PASSWORD_RESET_VIEW_SCHEMA
class PasswordResetView(APIView):
    """Восстановление пароля по email."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        # Генерация нового пароля
        new_password = get_random_string(length=8)
        user.set_password(new_password)
        user.save()

        # Отправка нового пароля по email
        send_reset_password_email.delay(new_password, email)

        return Response(
            {"message": "Новый пароль отправлен на email"},
            status=status.HTTP_200_OK
        )


@GAZPROMUSER_SCHEMA
@extend_schema(tags=["users"])
class UserViewSet(BaseViewSet):
    """Представление для пользователей (сотрудников)."""

    queryset = User.objects.all()
    http_method_names = ("get", "post", "patch", "delete")
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = (
        "id",
        "employee_fio",
        "employee_telegram",
        "employee_telephone",
        "email",
        "gazpromuserteam__team__product__product_name",
        "employee_position",
        "employee_grade",
        "employee_location",
        "gazpromuserteam__team__team_name",
        "skills__name",
    )
    filterset_class = GazpromUserFilter

    def get_permissions(self):
        # Доступ к созданию и удалению пользователя
        # разрешаем только суперпользователю
        if self.action in ("create", "destroy"):
            return (IsSuperuser(),)
        # Доступ к редактированию профиля, загрузке и удалению аватара
        # разрешаем только суперпользователю и владельцу профиля
        elif self.action in (
                "partial_update", "upload_avatar", "delete_avatar"
        ):
            return (IsSuperuserOrProfileOwner(),)
        else:
            return (IsAuthenticated(),)

    def get_serializer_class(self):
        match self.action:
            case "retrieve" | "me":
                return EmployeeGetSerializer
            case "create":
                return EmployeeWriteSuperuserSerializer
            case "partial_update":
                if self.request.user.is_superuser:
                    return EmployeeWriteSuperuserSerializer
                return EmployeePatchUserSerializer
            case "upload_avatar":
                return AvatarUploadSerializer
            case "list":
                return EmployeeListSerializer
            case _:
                return super().get_serializer_class()

    @ME_SCHEMA
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @UPLOAD_AVATAR_SCHEMA
    @action(
        detail=True,
        methods=["patch"],
        url_path="upload-avatar",
        parser_classes=[parsers.MultiPartParser],
    )
    def upload_avatar(self, request, pk=None):
        """Добавление аватара пользователя."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @DELETE_AVATAR_SCHEMA
    @action(detail=True, methods=["delete"], url_path="delete-avatar")
    def delete_avatar(self, request, pk=None):
        """Удаление аватара сотрудника."""
        user = self.get_object()
        user.employee_avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """Вместо удаления изменяем сотруднику статус на 'уволен'"""
        instance.employee_status = "fired"
        instance.save()
