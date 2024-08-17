from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)

from departments.serializers import (
    DepartmentAddEmployeesSerializer,
    DepartmentChildrenReadSerializer,
)
from users.serializers import EmployeeShortGetSerializer

DEPARTMENT_SCHEMA = extend_schema_view(
    list=extend_schema(
        description="Получение списка департаментов и числа сотрудников",
        summary="Получение списка департаментов и числа сотрудников",
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
                description="Поиск департамента по полям: "
                "идентификатор, название, описание",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Получение информации о департаменте и числа сотрудников",
        summary="Получение информации о департаменте и числа сотрудников",
    ),
    create=extend_schema(
        description="Добавление нового департамента",
        summary="Добавление нового департамента",
    ),
    destroy=extend_schema(
        description="Удаление департамента", summary="Удаление департамента"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о департаменте",
        summary="Частичное изменение информации о департаменте",
    ),
    update=extend_schema(
        description="Изменение информации о департаменте",
        summary="Изменение информации о департаменте",
    ),
)

EMPLOYEES_SCHEMA = extend_schema(
    request=DepartmentAddEmployeesSerializer,
    responses={
        200: DepartmentAddEmployeesSerializer,
        204: DepartmentAddEmployeesSerializer,
        400: OpenApiResponse(
            description="Invalid data",
        ),
    },
    description="Добавление и удаление сотрудников из департамента.",
    summary="Добавление и удаление сотрудников из департамента.",
)

CHILDREN_DEPARTMENTS_SCHEMA = extend_schema(
    responses={
        200: DepartmentChildrenReadSerializer(many=True),
        404: OpenApiResponse(
            description="No Department matches the given query.",
        ),
    },
    description="Получение списка дочерних департаментов.",
    summary="Получение списка дочерних департаментов.",
)

EMPLOYEES_LIST_SCHEMA = extend_schema(
    responses={
        200: EmployeeShortGetSerializer(many=True),
        404: OpenApiResponse(
            description="No Department matches the given query.",
        ),
    },
    description="Получение списка сотрудников.",
    summary="Получение списка сотрудников.",
)

ROOT_DEPARTMENTS_SCHEMA = extend_schema(
    responses={
        200: DepartmentChildrenReadSerializer(many=True),
        404: OpenApiResponse(
            description="No Department matches the given query.",
        ),
    },
    description="Получение списка департаментов, "
    "не имеющих родительских департаментов.",
    summary="Получение списка корневых департаментов.",
)
