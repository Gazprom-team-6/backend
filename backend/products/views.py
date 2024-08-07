from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import viewsets
from rest_framework.decorators import action

from company.permissions import IsSuperuserOrReadOnly
from products.models import Product
from products.serializers import (ProductChildrenReadSerializer,
                                  ProductReadSerializer,
                                  ProductWriteSerializer)
from teams.models import Team
from teams.serializers import TeamListSerializer


@extend_schema_view(
    list=extend_schema(
        description="Получение списка продуктов",
        summary="Получение списка продуктов"
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
@extend_schema(tags=["product"])
class ProductViewSet(viewsets.ModelViewSet):
    """Представление для продуктов."""

    permission_classes = [IsSuperuserOrReadOnly, ]

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "product_manager",
                "parent_product"
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProductWriteSerializer
        elif self.action == "children_products":
            return ProductChildrenReadSerializer
        elif self.action == "product_teams":
            return TeamListSerializer
        return ProductReadSerializer

    @extend_schema(
        responses={
            200: ProductChildrenReadSerializer(many=True),
            404: OpenApiResponse(
                description="No Product matches the given query.",
            )
        },
        description="Получение списка дочерних продуктов.",
        summary="Получение списка дочерних продуктов."
    )
    @action(["get"], detail=True, url_path="subsidiary")
    def children_products(self, request, pk=None):
        """Получение списка дочерних продуктов."""
        parent_product = self.get_object()
        children = Product.objects.filter(
            parent_product=parent_product
        )
        page = self.paginate_queryset(children)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            200: ProductChildrenReadSerializer(many=True),
            404: OpenApiResponse(
                description="No Product matches the given query.",
            )
        },
        description="Получение списка продуктов, "
                    "не имеющих родительских продуктов.",
        summary="Получение списка корневых продуктов."
    )
    @action(["get"], detail=False, url_path="root_products")
    def root_products(self, request, pk=None):
        """Получение списка корневых продуктов."""
        departments = Product.objects.filter(
            parent_product=None
        )
        page = self.paginate_queryset(departments)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            200: TeamListSerializer(many=True),
            404: OpenApiResponse(
                description="No Product matches the given query.",
            )
        },
        description="Получение списка команд продукта.",
        summary="Получение списка команд продукта."
    )
    @action(["get"], detail=True, url_path="product_teams")
    def product_teams(self, request, pk=None):
        """Получение списка команд продукта."""
        product = self.get_object()
        teams = Team.objects.filter(
            product=product
        )
        page = self.paginate_queryset(teams)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
