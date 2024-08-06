from django.contrib.auth import get_user_model
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiResponse)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from company.models import Department, Product
from company.permissions import IsSuperuserOrReadOnly
from company.serializers import (DepartmentAddEmployeesSerializer,
                                 DepartmentChildrenReadSerializer,
                                 DepartmentReadSerializer,
                                 DepartmentWriteSerializer,
                                 EmployeeListResponseSerializer,
                                 ProductChildrenReadSerializer,
                                 ProductReadSerializer,
                                 ProductWriteSerializer)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description="Получение списка департаментов",
        summary="Получение списка департаментов"
    ),
    retrieve=extend_schema(
        description="Получение информации о департаменте",
        summary="Получение информации о департаменте"
    ),
    create=extend_schema(
        description="Добавление нового департамента",
        summary="Добавление нового департамента"
    ),
    destroy=extend_schema(
        description="Удаление департамента",
        summary="Удаление департамента"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о департаменте",
        summary="Частичное изменение информации о департаменте"
    ),
    update=extend_schema(
        description="Изменение информации о департаменте",
        summary="Изменение информации о департаменте"
    ),
)
@extend_schema(tags=["department"])
class DepartmentViewSet(viewsets.ModelViewSet):
    """Представление для департаментов."""

    permission_classes = [IsSuperuserOrReadOnly, ]

    def get_queryset(self):
        queryset = Department.objects.all()
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
            return EmployeeListResponseSerializer
        else:
            return DepartmentWriteSerializer

    @extend_schema(
        request=DepartmentAddEmployeesSerializer,
        responses={
            200: DepartmentAddEmployeesSerializer,
            204: DepartmentAddEmployeesSerializer,
            400: OpenApiResponse(
                description="Invalid data",
            )
        },
        description="Добавление и удаление сотрудников из департамента.",
        summary="Добавление и удаление сотрудников из департамента."
    )
    @action(["post", "delete"], detail=True, url_path='employees')
    def employees(self, request, pk=None):
        """Добавление и удаление сотрудников из департамента."""
        department = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data['employee_ids']
            employees = User.objects.filter(id__in=employee_ids)
            if request.method == 'POST':
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

    @extend_schema(
        responses={
            200: DepartmentChildrenReadSerializer(many=True),
            404: OpenApiResponse(
                description="No Department matches the given query.",
            )
        },
        description="Получение списка дочерних департаментов.",
        summary="Получение списка дочерних департаментов."
    )
    @action(["get"], detail=True, url_path='subsidiary')
    def children_departments(self, request, pk=None):
        """Получение списка дочерних департаментов."""
        parent_department = self.get_object()
        children = Department.objects.filter(
            parent_department=parent_department
        )
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: EmployeeListResponseSerializer(),
            404: OpenApiResponse(
                description="No Department matches the given query.",
            )
        },
        description="Получение списка сотрудников.",
        summary="Получение списка сотрудников."
    )
    @action(["get"], detail=True, url_path='employees_list')
    def employees_list(self, request, pk=None):
        """Получение списка сотрудников."""
        department = self.get_object()
        employees = User.objects.filter(employee_departament=department)
        total_employees = employees.count()

        response_data = {
            'total_employees': total_employees,
            'employees': employees
        }

        serializer = self.get_serializer(response_data)
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: DepartmentChildrenReadSerializer(many=True),
            404: OpenApiResponse(
                description="No Department matches the given query.",
            )
        },
        description="Получение списка департаментов, "
                    "не имеющих родительских департаментов.",
        summary="Получение списка корневых департаментов."
    )
    @action(["get"], detail=False, url_path='root_departments')
    def root_departments(self, request, pk=None):
        """Получение списка корневых департаментов."""
        departments = Department.objects.filter(
            parent_department=None
        )
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)


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
    @action(["get"], detail=True, url_path='subsidiary')
    def children_products(self, request, pk=None):
        """Получение списка дочерних продуктов."""
        parent_product = self.get_object()
        children = Product.objects.filter(
            parent_product=parent_product
        )
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

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
    @action(["get"], detail=False, url_path='root_products')
    def root_products(self, request, pk=None):
        """Получение списка корневых продуктов."""
        departments = Product.objects.filter(
            parent_product=None
        )
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)

