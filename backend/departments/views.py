from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from drf_spectacular.utils import (extend_schema)
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from company.mixins import BaseViewSet
from company.permissions import IsSuperuserOrReadOnly
from departments.models import Department
from departments.schemas import (CHILDREN_DEPARTMENTS_SCHEMA,
                                 DEPARTMENT_SCHEMA,
                                 EMPLOYEES_LIST_SCHEMA, EMPLOYEES_SCHEMA,
                                 ROOT_DEPARTMENTS_SCHEMA)
from departments.serializers import (DepartmentAddEmployeesSerializer,
                                     DepartmentChildrenReadSerializer,
                                     DepartmentReadSerializer,
                                     DepartmentWriteSerializer)
from users.serializers import EmployeeShortGetSerializer

User = get_user_model()


# Create your views here.
@DEPARTMENT_SCHEMA
@extend_schema(tags=["department"])
class DepartmentViewSet(BaseViewSet):
    """Представление для департаментов."""

    permission_classes = [IsSuperuserOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "departament_name", "departament_description")

    def get_queryset(self):
        queryset = Department.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "departament_owner",
                "parent_department"
            ).only(
                "id",
                "departament_name",
                "departament_description",
                "departament_owner__id",
                "departament_owner__employee_fio",
                "departament_owner__employee_avatar",
                "departament_owner__employee_position",
                "departament_owner__employee_grade",
                "parent_department__id",
                "parent_department__departament_name",
                "parent_department__departament_owner",
            ).annotate(employee_count=Count('users'))
        if self.action in ("root_departments", "children_departments"):
            queryset = queryset.select_related(
                "departament_owner"
            ).only(
                "id",
                "departament_name",
                "departament_description",
                "departament_owner__id",
                "departament_owner__employee_fio",
                "departament_owner__employee_avatar",
                "departament_owner__employee_position",
                "departament_owner__employee_grade",
            ).annotate(employee_count=Count('users'))
        return queryset

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return DepartmentReadSerializer
        elif self.action in ("children_departments", "root_departments"):
            return DepartmentChildrenReadSerializer
        elif self.action == "employees":
            return DepartmentAddEmployeesSerializer
        elif self.action == "employees_list":
            return EmployeeShortGetSerializer
        elif self.action in ("create", "update", "partial_update"):
            return DepartmentWriteSerializer
        return super().get_serializer_class()

    @EMPLOYEES_SCHEMA
    @transaction.atomic
    @action(["post", "delete"], detail=True, url_path="employees")
    def employees(self, request, pk=None):
        """Добавление и удаление сотрудников из департамента."""
        department = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee_ids = serializer.validated_data["employee_ids"]
        employees = User.objects.filter(id__in=employee_ids)
        if request.method == "POST":
            employees.update(employee_departament=department)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            employees.update(employee_departament=None)
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    @CHILDREN_DEPARTMENTS_SCHEMA
    @action(["get"], detail=True, url_path="subsidiary")
    def children_departments(self, request, pk=None):
        """Получение списка дочерних департаментов."""
        department = self.get_object()
        children = self.get_queryset().filter(
            parent_department=department
        )
        return self.get_paginated_data(
            request=request,
            queryset=children
        )

    @EMPLOYEES_LIST_SCHEMA
    @action(["get"], detail=True, url_path="employees_list")
    def employees_list(self, request, pk=None):
        """Получение списка сотрудников."""
        department = self.get_object()
        employees = User.objects.filter(
            employee_departament=department
        ).only(
            "id",
            "employee_fio",
            "employee_avatar",
            "employee_position",
            "employee_grade"
        )
        return self.get_paginated_data(
            request=request,
            queryset=employees
        )

    @ROOT_DEPARTMENTS_SCHEMA
    @action(["get"], detail=False, url_path="root_departments")
    def root_departments(self, request):
        """Получение списка корневых департаментов."""
        departments = self.get_queryset().filter(
                parent_department=None
            )
        return self.get_paginated_data(
            request=request,
            queryset=departments
        )
