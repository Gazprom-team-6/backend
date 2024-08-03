from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsSuperuser, IsSuperuserOrProfileOwner
from users.serializers import (AvatarUploadSerializer, PasswordResetSerializer,
                               ProfileListSerializer,
                               ProfilePatchUserSerializer,
                               ProfileGetSerializer,
                               ProfileWriteSuperuserSerializer)

User = get_user_model()


@extend_schema(
    tags=['usersauth'],
    request=PasswordResetSerializer,
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    description="Позволяет неавторизованному пользователю восстановить "
                "пароль, если его email зарегистрирован в системе. "
                "Система генерирует и присылает новый пароль на "
                "указанный email.",
    examples=[
        OpenApiExample(
            name='Success Response',
            value={"message": "Новый пароль отправлен на email"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name='Bad Request Response',
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
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Генерация нового пароля
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            # Отправка нового пароля по email
            send_mail(
                'Восстановление пароля',
                f'Ваш новый пароль: {new_password}',
                'no-reply@yourdomain.com',
                [email],
                fail_silently=False,
            )

            return Response(
                {"message": "Новый пароль отправлен на email"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление для пользователей (сотрудников)."""

    queryset = User.objects.all()
    http_method_names = ("get", "post", "patch")

    def get_permissions(self):
        if self.action == "create":
            return (IsSuperuser(),)
        elif self.action in ("partial_update", "upload_avatar"):
            return (IsSuperuserOrProfileOwner(),)
        else:
            return IsAuthenticated

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileGetSerializer
        elif self.action == "create":
            return ProfileWriteSuperuserSerializer
        elif self.action == "partial_update":
            if self.request.user.is_superuser:
                return ProfileWriteSuperuserSerializer
            return ProfilePatchUserSerializer
        elif self.action == "upload_avatar":
            return AvatarUploadSerializer
        else:
            return ProfileListSerializer

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        # self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], url_path="upload-avatar")
    def upload_avatar(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



