from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter, OpenApiResponse)

from teams.serializers import (TeamAddEmployeesSerializer,
                               TeamDeleteEmployeesSerializer,
                               TeamEmployeeChangeRoleSerializer,
                               TeamEmployeeListSerializer)

TEAM_SCHEMA = extend_schema_view(
    list=extend_schema(
        description="Получение списка команд и числа сотрудников",
        summary="Получение списка команд и числа сотрудников",
        parameters=[
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
            OpenApiParameter(
                name="search",
                description="Поиск команд по полям: "
                            "идентификатор, название",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ]
    ),
    retrieve=extend_schema(
        description="Получение информации о команде и о числе сотрудников",
        summary="Получение информации о команде и о числе сотрудников"
    ),
    create=extend_schema(
        description="Добавление новой команды",
        summary="Добавление новой команды"
    ),
    destroy=extend_schema(
        description="Удаление команды",
        summary="Удаление команды"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о команде",
        summary="Частичное изменение информации о команде"
    ),
    update=extend_schema(
        description="Изменение информации о команде",
        summary="Изменение информации о команде"
    ),
)

EMPLOYEES_LIST_SCHEMA = extend_schema(
    responses={
        200: TeamEmployeeListSerializer(many=True),
        404: OpenApiResponse(
            description="No Team matches the given query.",
        )
    },
    description="Получение списка сотрудников.",
    summary="Получение списка сотрудников."
)

ADD_EMPLOYEES_SCHEMA = extend_schema(
    request=TeamAddEmployeesSerializer,
    responses={
        200: TeamAddEmployeesSerializer,
        400: OpenApiResponse(
            description="Invalid data",
        )
    },
    description="Добавление сотрудников в команду.",
    summary="Добавление сотрудников в команду."
)

REMOVE_EMPLOYEES_SCHEMA = extend_schema(
    request=TeamDeleteEmployeesSerializer,
    responses={
        204: TeamDeleteEmployeesSerializer,
        400: OpenApiResponse(
            description="Invalid data",
        )
    },
    description="Удаление сотрудников из команды.",
    summary="Удаление сотрудников из команды."
)

CHANGE_EMPLOYEE_ROLE_SCHEMA = extend_schema(
    request=TeamEmployeeChangeRoleSerializer,
    responses={
        200: TeamEmployeeChangeRoleSerializer,
        400: OpenApiResponse(
            description="Invalid data",
        ),
        404: OpenApiResponse(
            description="No Object matches the given query."
        )
    },
    description="Изменение роли пользователя в команде.",
    summary="Изменение роли пользователя в команде."
)
