from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   PolymorphicProxySerializer, extend_schema,
                                   extend_schema_view)
from rest_framework import parsers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsSuperuser, IsSuperuserOrProfileOwner
from users.serializers import (AvatarUploadSerializer, EmployeeGetSerializer,
                               EmployeeListSerializer,
                               EmployeePatchUserSerializer,
                               EmployeeWriteSuperuserSerializer,
                               PasswordResetSerializer)

User = get_user_model()


@extend_schema(
    tags=["usersauth"],
    request=PasswordResetSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    description="Позволяет неавторизованному пользователю восстановить "
                "пароль, если его email зарегистрирован в системе. "
                "Система генерирует и присылает новый пароль на "
                "указанный email.",
    summary="Восстановление пароля.",
    examples=[
        OpenApiExample(
            name="Success Response",
            value={"message": "Новый пароль отправлен на email"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Bad Request Response",
            value={"email": ["Это поле является обязательным"]},
            response_only=True,
            status_codes=["400"],
        )
    ],
)
class PasswordResetView(APIView):
    """Восстановление пароля по email."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Генерация нового пароля
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            # Отправка нового пароля по email
            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                "no-reply@yourdomain.com",
                [email],
                fail_silently=False,
            )

            return Response(
                {"message": "Новый пароль отправлен на email"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        description="Получение списка сотрудников",
        summary="Получение списка сотрудников."
    ),
    retrieve=extend_schema(
        description="Получение информации о сотруднике",
        summary="Получение информации о сотруднике."
    ),
    create=extend_schema(
        description="Добавление нового сотрудника",
        summary="Добавление нового сотрудника."
    ),
    destroy=extend_schema(
        description="Увольнение сотрудника. "
                    "Статус сотрудника меняется на Уволен",
        summary="Увольнение сотрудника."
    ),
    partial_update=extend_schema(
        responses=PolymorphicProxySerializer(
            component_name='IsSuperuser',
            serializers=[
                EmployeeWriteSuperuserSerializer, EmployeePatchUserSerializer,
            ],
            resource_type_field_name='is_superuser',
        ),
        request=PolymorphicProxySerializer(
            component_name='IsSuperuser',
            serializers=[
                EmployeeWriteSuperuserSerializer, EmployeePatchUserSerializer,
            ],
            resource_type_field_name='is_superuser',
        ),
        description="Изменение информации о сотруднике.",
        summary="Изменение информации о сотруднике."
    ),

)
@extend_schema(tags=["users"])
class UserViewSet(viewsets.ModelViewSet):
    """Представление для пользователей (сотрудников)."""

    queryset = User.objects.all()
    http_method_names = ("get", "post", "patch", "delete")

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
        if self.action in ("retrieve", "me"):
            return EmployeeGetSerializer
        elif self.action == "create":
            return EmployeeWriteSuperuserSerializer
        elif self.action == "partial_update":
            if self.request.user.is_superuser:
                return EmployeeWriteSuperuserSerializer
            return EmployeePatchUserSerializer
        elif self.action == "upload_avatar":
            return AvatarUploadSerializer
        else:
            return EmployeeListSerializer

    @extend_schema(
        responses={200: EmployeeGetSerializer},
        description="Просмотр информации о пользователей.",
        summary="Просмотр информации о пользователей."
    )
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @extend_schema(
        request=AvatarUploadSerializer,
        responses={200: AvatarUploadSerializer},
        description="Загрузка аватара сотрудника. "
                    "Файл должен быть  формата formdata",
        summary="Загрузка аватара сотрудника."
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="upload-avatar",
        parser_classes=[parsers.MultiPartParser]
    )
    def upload_avatar(self, request, pk=None):
        """Добавление аватара пользователя."""
        user = self.get_object()
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(
                description="Аватар успешно удален",
            ),
        },
        description="Удаление аватара сотрудника.",
        summary="Удаление аватара сотрудника."
    )
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
