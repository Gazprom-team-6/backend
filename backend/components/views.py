from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters

from company.mixins import BaseViewSet
from company.permissions import IsSuperuserOrReadOnly
from components.models import Component
from components.schemas import COMPONENT_SCHEMA
from components.serializers import (ComponentReadSerializer,
                                    ComponentWriteSerializer)


@COMPONENT_SCHEMA
@extend_schema(tags=["component"])
class ComponentViewSet(BaseViewSet):
    """Представление для компонента."""

    permission_classes = [
        IsSuperuserOrReadOnly,
    ]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = (
        "id",
        "component_name",
        "component_owner__employee_fio",
        "component_description",
    )
    filterset_fields = ("component_type",)

    def get_queryset(self):
        queryset = Component.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "component_owner",
                "component_second_owner",
            ).only(
                "id",
                "component_name",
                "component_type",
                "component_link",
                "component_description",
                "component_owner__employee_fio",
                "component_owner__id",
                "component_second_owner__employee_fio",
                "component_second_owner__id",
            )
        return queryset

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return ComponentWriteSerializer
            case "list" | "retrieve":
                return ComponentReadSerializer
            case _:
                return super().get_serializer_class()
