from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import PasswordResetSerializer


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
