from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, PolymorphicProxySerializer,
                                   extend_schema, extend_schema_view)

from users.serializers import (AvatarUploadSerializer, EmployeeGetSerializer,
                               EmployeePatchUserSerializer,
                               EmployeeWriteSuperuserSerializer,
                               PasswordResetSerializer)

GAZPROMUSER_SCHEMA = extend_schema_view(
    list=extend_schema(
        description="Получение списка сотрудников",
        summary="Получение списка сотрудников.",
        parameters=[
            OpenApiParameter(
                name="department",
                description="Фильтр по названию департамента",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="is_outsource",
                description="Фильтр по статусу outsource",
                required=False,
                type=OpenApiTypes.BOOL,
            ),
            OpenApiParameter(
                name="location",
                description="Фильтр по статусу локации (часовому поясу)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="position",
                description="Фильтр по должности сотрудника",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="location",
                description="Фильтр по статусу локации (часовому поясу)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="product",
                description="Фильтр по продукту, в котором принимает участие "
                            "сотрудник",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="search",
                description="Поиск сотрудника по полям: идентификатор, "
                            "ФИО сотрудника, название отдела, должность, "
                            "email, грейд, название продукта, "
                            "локация (часовой пояс), название компонента, "
                            "тип занятости, название команды, навыки, статус",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="skill",
                description="Фильтр по навыка. Могут быть переданы несколько "
                            "навыков в формате: ?skill=skill1&skill=skill2",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="team",
                description="Фильтр по названию команды",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="limit",
                description="Ограничение количества результатов в ответе.",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="offset",
                description="Начальная позиция в списке результатов.",
                required=False,
                type=OpenApiTypes.INT,
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Получение информации о сотруднике",
        summary="Получение информации о сотруднике.",
    ),
    create=extend_schema(
        description="Добавление нового сотрудника",
        summary="Добавление нового сотрудника.",
        request=EmployeeWriteSuperuserSerializer,
    ),
    destroy=extend_schema(
        description="Увольнение сотрудника. "
                    "Статус сотрудника меняется на Уволен",
        summary="Увольнение сотрудника.",
    ),
    partial_update=extend_schema(
        responses=PolymorphicProxySerializer(
            component_name="IsSuperuser",
            serializers=[
                EmployeeWriteSuperuserSerializer,
                EmployeePatchUserSerializer,
            ],
            resource_type_field_name="is_superuser",
        ),
        request=PolymorphicProxySerializer(
            component_name="IsSuperuser",
            serializers=[
                EmployeeWriteSuperuserSerializer,
                EmployeePatchUserSerializer,
            ],
            resource_type_field_name="is_superuser",
        ),
        description="Изменение информации о сотруднике.",
        summary="Изменение информации о сотруднике.",
    ),
)

PASSWORD_RESET_VIEW_SCHEMA = extend_schema(
    tags=["users"],
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
        ),
    ],
)

ME_SCHEMA = extend_schema(
    responses={200: EmployeeGetSerializer},
    description="Просмотр информации о пользователей.",
    summary="Просмотр информации о пользователей.",
)

UPLOAD_AVATAR_SCHEMA = extend_schema(
    request=AvatarUploadSerializer,
    responses={200: AvatarUploadSerializer},
    description="Загрузка аватара сотрудника. "
                "Файл должен быть  формата formdata",
    summary="Загрузка аватара сотрудника.",
)

DELETE_AVATAR_SCHEMA = extend_schema(
    responses={
        204: OpenApiResponse(
            description="Аватар успешно удален",
        ),
    },
    description="Удаление аватара сотрудника.",
    summary="Удаление аватара сотрудника.",
)
