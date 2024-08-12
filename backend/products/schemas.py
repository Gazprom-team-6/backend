from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter, OpenApiResponse)

from components.serializers import ComponentReadSerializer
from products.serializers import (ProductChildrenReadSerializer,
                                  ProductListSerializer, ProductRootSerializer)
from teams.serializers import TeamListSerializer

PRODUCT_SCHEMA = extend_schema_view(
    list=extend_schema(
        description="Получение списка продуктов",
        summary="Получение списка продуктов",
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
                            "идентификатор, название, описание",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ]
    ),
    retrieve=extend_schema(
        description="Получение информации о продукте",
        summary="Получение информации о продукте"
    ),
    create=extend_schema(
        description="Добавление нового продукта",
        summary="Добавление нового продукта"
    ),
    destroy=extend_schema(
        description="Удаление продукта",
        summary="Удаление продукта"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о продукте",
        summary="Частичное изменение информации о продукте"
    ),
    update=extend_schema(
        description="Изменение информации о продукте",
        summary="Изменение информации о продукте"
    ),
)

CHILDREN_PRODUCTS_SCHEMA = extend_schema(
    responses={
        200: ProductChildrenReadSerializer(many=True),
        404: OpenApiResponse(
            description="No Product matches the given query.",
        )
    },
    description="Получение списка дочерних продуктов.",
    summary="Получение списка дочерних продуктов."
)

ROOT_PRODUCTS_SCHEMA = extend_schema(
    responses={
        200: ProductRootSerializer(many=True),
        404: OpenApiResponse(
            description="No Product matches the given query.",
        )
    },
    description="Получение списка продуктов, "
                "не имеющих родительских продуктов.",
    summary="Получение списка корневых продуктов."
)

PRODUCT_TEAMS_SCHEMA = extend_schema(
    responses={
        200: TeamListSerializer(many=True),
        404: OpenApiResponse(
            description="No Product matches the given query.",
        )
    },
    description="Получение списка команд продукта.",
    summary="Получение списка команд продукта."
)

PRODUCT_COMPONENTS_SCHEMA = extend_schema(
    responses={
        200: ComponentReadSerializer(many=True),
        404: OpenApiResponse(
            description="No Product matches the given query.",
        )
    },
    description="Получение списка компонентов продукта.",
    summary="Получение списка компонентов продукта."
)
