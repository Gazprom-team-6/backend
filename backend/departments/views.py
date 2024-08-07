from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
class DepartmentViewSet(viewsets.ModelViewSet):
    """Представление для департаментов."""

    permission_classes = [IsSuperuserOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "departament_name", "departament_description")

    def get_queryset(self):
        # Добавляем подсчет числа сотрудников в департаменте
        queryset = Department.objects.annotate(employee_count=Count('users'))
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "departament_owner",
                "parent_department"
            )
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
        else:
            return DepartmentWriteSerializer

    @EMPLOYEES_SCHEMA
    @action(["post", "delete"], detail=True, url_path="employees")
    def employees(self, request, pk=None):
        """Добавление и удаление сотрудников из департамента."""
        department = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
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
                    serializer.data,
                    status=status.HTTP_204_NO_CONTENT
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @CHILDREN_DEPARTMENTS_SCHEMA
    @action(["get"], detail=True, url_path="subsidiary")
    def children_departments(self, request, pk=None):
        """Получение списка дочерних департаментов."""
        parent_department = self.get_object()
        children = Department.objects.filter(
            parent_department=parent_department
        )
        page = self.paginate_queryset(children)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @EMPLOYEES_LIST_SCHEMA
    @action(["get"], detail=True, url_path="employees_list")
    def employees_list(self, request, pk=None):
        """Получение списка сотрудников."""
        department = self.get_object()
        employees = User.objects.filter(employee_departament=department)
        page = self.paginate_queryset(employees)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @ROOT_DEPARTMENTS_SCHEMA
    @action(["get"], detail=False, url_path="root_departments")
    def root_departments(self, request, pk=None):
        """Получение списка корневых департаментов."""
        departments = Department.objects.filter(
            parent_department=None
        )
        page = self.paginate_queryset(departments)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
