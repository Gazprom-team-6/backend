from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (extend_schema,
                                   extend_schema_view)
from rest_framework import filters, viewsets

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

    permission_classes = [IsSuperuserOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ("id", "component_name", "component_owner__employee_fio",
                     "component_description")
    filterset_fields = ("component_type",)

    def get_queryset(self):
        queryset = Component.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "component_owner",
                "component_second_owner",
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ComponentWriteSerializer
        elif self.action in ("list", "retrieve"):
            return ComponentReadSerializer
        return super().get_serializer_class()
