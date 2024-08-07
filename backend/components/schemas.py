from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter)

COMPONENT_SCHEMA = extend_schema_view(
    list=extend_schema(
        description="Получение списка компонентов",
        summary="Получение списка компонентов",
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
                description="Поиск продукта по полям: "
                            "идентификатор, название, описание, "
                            "ФИО ответственного сотрудника",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="component_type",
                description="Фильтр по типу компонента",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ]
    ),
    retrieve=extend_schema(
        description="Получение информации о компоненте",
        summary="Получение информации о компоненте"
    ),
    create=extend_schema(
        description="Добавление нового компонента",
        summary="Добавление нового компонента"
    ),
    destroy=extend_schema(
        description="Удаление компонента",
        summary="Удаление компонента"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о компоненте",
        summary="Частичное изменение информации о компоненте"
    ),
    update=extend_schema(
        description="Изменение информации о компоненте",
        summary="Изменение информации о компоненте"
    ),
)
