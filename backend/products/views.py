from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import filters
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
                                  ProductGetSerializer, ProductListSerializer,
                                  ProductRootSerializer,
                                  ProductWriteSerializer)
from teams.models import Team
from teams.serializers import TeamListSerializer


@PRODUCT_SCHEMA
@extend_schema(tags=["product"])
class ProductViewSet(BaseViewSet):
    """Представление для продуктов."""

    permission_classes = [
        IsSuperuserOrReadOnly,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "product_name", "product_description")

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "product_manager",
            ).prefetch_related(
                Prefetch(
                    "components",
                    queryset=Component.objects.all().only(
                        "id", "component_name"
                    ),
                )
            )
            if self.action == "retrieve":
                queryset = (
                    queryset.select_related("parent_product")
                    .prefetch_related(
                        Prefetch(
                            "parent_product__components",
                            queryset=Component.objects.all().only(
                                "id",
                            ),
                        )
                    )
                    .only(
                        "id",
                        "product_name",
                        "product_description",
                        "product_manager__id",
                        "product_manager__employee_fio",
                        "product_manager__employee_avatar",
                        "product_manager__employee_position",
                        "product_manager__employee_grade",
                        "parent_product__id",
                        "parent_product__product_name",
                        "parent_product__product_description",
                        "parent_product__product_manager",
                        "parent_product__parent_product",
                        "parent_product__components",
                    )
                )
            else:
                queryset = queryset.only(
                    "id",
                    "product_name",
                    "product_description",
                    "parent_product",
                    "product_manager__id",
                    "product_manager__employee_fio",
                    "product_manager__employee_avatar",
                    "product_manager__employee_position",
                    "product_manager__employee_grade",
                )
        elif self.action in ("children_products", "root_products"):
            queryset = queryset.select_related("product_manager").only(
                "id",
                "product_name",
                "product_description",
                "product_manager__id",
                "product_manager__employee_fio",
                "product_manager__employee_avatar",
                "product_manager__employee_position",
                "product_manager__employee_grade",
            )
            if self.action == "root_products":
                queryset = queryset.prefetch_related(
                    Prefetch(
                        "components",
                        queryset=Component.objects.all().only(
                            "id", "component_name"
                        ),
                    )
                )
        return queryset

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return ProductWriteSerializer
            case "children_products":
                return ProductChildrenReadSerializer
            case "product_teams":
                return TeamListSerializer
            case "retrieve":
                return ProductGetSerializer
            case "list":
                return ProductListSerializer
            case "root_products":
                return ProductRootSerializer
            case "product_components":
                return ComponentReadSerializer
            case _:
                return super().get_serializer_class()

    @CHILDREN_PRODUCTS_SCHEMA
    @action(["get"], detail=True, url_path="subsidiary")
    def children_products(self, request, pk=None):
        """Получение списка дочерних продуктов."""
        product = self.get_object()
        children = self.get_queryset().filter(parent_product=product)
        return self.get_paginated_data(request=request, queryset=children)

    @ROOT_PRODUCTS_SCHEMA
    @action(["get"], detail=False, url_path="root_products")
    def root_products(self, request, pk=None):
        """Получение списка корневых продуктов."""
        products = self.get_queryset().filter(parent_product=None)
        return self.get_paginated_data(request=request, queryset=products)

    @PRODUCT_TEAMS_SCHEMA
    @action(["get"], detail=True, url_path="product_teams")
    def product_teams(self, request, pk=None):
        """Получение списка команд продукта."""
        product = self.get_object()
        teams = (
            Team.objects.filter(product=product)
            .select_related("team_manager")
            .only(
                "id",
                "team_name",
                "product",
                "team_manager__id",
                "team_manager__employee_fio",
                "team_manager__employee_avatar",
                "team_manager__employee_position",
                "team_manager__employee_grade",
            )
        )
        return self.get_paginated_data(request=request, queryset=teams)

    @PRODUCT_COMPONENTS_SCHEMA
    @action(["get"], detail=True, url_path="product_components")
    def product_components(self, request, pk=None):
        """Получение списка компонентов продукта."""
        product = self.get_object()
        components = (
            product.components.all()
            .select_related("component_owner", "component_second_owner")
            .only(
                "id",
                "component_name",
                "component_type",
                "component_link",
                "component_description",
                "component_owner__id",
                "component_owner__employee_fio",
                "component_second_owner__id",
                "component_second_owner__employee_fio",
            )
        )
        return self.get_paginated_data(request=request, queryset=components)
