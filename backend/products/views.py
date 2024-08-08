from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import filters, viewsets
from rest_framework.decorators import action

from company.mixins import BaseViewSet
from company.permissions import IsSuperuserOrReadOnly
from components.models import Component
from components.serializers import ComponentReadSerializer
from products.models import Product
from products.schemas import (CHILDREN_PRODUCTS_SCHEMA,
                              PRODUCT_COMPONENTS_SCHEMA, PRODUCT_SCHEMA,
                              PRODUCT_TEAMS_SCHEMA, ROOT_PRODUCTS_SCHEMA)
from products.serializers import (ProductChildrenReadSerializer,
                                  ProductGetSerializer,
                                  ProductListSerializer,
                                  ProductWriteSerializer)
from teams.models import Team
from teams.serializers import TeamListSerializer


@PRODUCT_SCHEMA
@extend_schema(tags=["product"])
class ProductViewSet(BaseViewSet):
    """Представление для продуктов."""

    permission_classes = [IsSuperuserOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "product_name", "product_description")

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
        elif self.action == "retrieve":
            return ProductGetSerializer
        elif self.action == "product_components":
            return ComponentReadSerializer
        elif self.action in ("list", "root_products"):
            return ProductListSerializer
        return super().get_serializer_class()

    @CHILDREN_PRODUCTS_SCHEMA
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

    @ROOT_PRODUCTS_SCHEMA
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

    @PRODUCT_TEAMS_SCHEMA
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

    @PRODUCT_COMPONENTS_SCHEMA
    @action(["get"], detail=True, url_path="product_components")
    def product_components(self, request, pk=None):
        """Получение списка команд продукта."""
        product = self.get_object()
        components = product.components.all()
        page = self.paginate_queryset(components)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
