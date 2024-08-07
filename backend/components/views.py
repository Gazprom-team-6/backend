from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (extend_schema,
                                   extend_schema_view)
from rest_framework import filters, viewsets

from company.permissions import IsSuperuserOrReadOnly
from components.models import Component
from components.serializers import (ComponentReadSerializer,
                                    ComponentWriteSerializer)


@extend_schema_view(
    list=extend_schema(
        description="Получение списка компонентов",
        summary="Получение списка компонентов"
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
@extend_schema(tags=["component"])
class ComponentViewSet(viewsets.ModelViewSet):
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
        return ComponentReadSerializer
