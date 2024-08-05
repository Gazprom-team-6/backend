from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from company.models import Department
from company.permissions import IsSuperuserOrReadOnly
from company.serializers import (DepartmentReadSerializer,
                                 DepartmentWriteSerializer)


@extend_schema_view(
    list=extend_schema(description="Получение списка департаментов"),
    retrieve=extend_schema(description="Получение информации о департаменте"),
    create=extend_schema(description="Добавление нового департамента"),
    destroy=extend_schema(description="Удаление департамента"),
    partial_update=extend_schema(description="Изменение информации о департаменте"),
)
@extend_schema(tags=["department"])
class DepartmentViewSet(viewsets.ModelViewSet):
    """Представление для департаментов."""

    queryset = Department.objects.all()
    permission_classes = [IsSuperuserOrReadOnly,]

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return DepartmentReadSerializer
        return DepartmentWriteSerializer

