from django.contrib.auth import get_user_model
from django.db.models import Count
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiResponse)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from company.models import Department, GazpromUserTeam, Product, Team
from company.permissions import IsSuperuserOrReadOnly
from company.serializers import (DepartmentAddEmployeesSerializer,
                                 DepartmentChildrenReadSerializer,
                                 DepartmentReadSerializer,
                                 DepartmentWriteSerializer,
                                 ProductChildrenReadSerializer,
                                 ProductReadSerializer,
                                 ProductWriteSerializer,
                                 TeamAddEmployeesSerializer,
                                 TeamDeleteEmployeesSerializer,
                                 TeamEmployeeListSerializer, TeamGetSerializer,
                                 TeamListSerializer,
                                 TeamWriteSerializer)
from users.serializers import EmployeeShortGetSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description="Получение списка департаментов и числа сотрудников",
        summary="Получение списка департаментов и числа сотрудников"
    ),
    retrieve=extend_schema(
        description="Получение информации о департаменте и числа сотрудников",
        summary="Получение информации о департаменте и числа сотрудников"
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

    @extend_schema(
        responses={
            200: EmployeeShortGetSerializer(many=True),
            404: OpenApiResponse(
                description="No Department matches the given query.",
            )
        },
        description="Получение списка сотрудников.",
        summary="Получение списка сотрудников."
    )
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


@extend_schema_view(
    list=extend_schema(
        description="Получение списка команд и числа сотрудников",
        summary="Получение списка команд и числа сотрудников"
    ),
    retrieve=extend_schema(
        description="Получение информации о команде и о числе сотрудников",
        summary="Получение информации о команде и о числе сотрудников"
    ),
    create=extend_schema(
        description="Добавление новой команды",
        summary="Добавление новой команды"
    ),
    destroy=extend_schema(
        description="Удаление команды",
        summary="Удаление команды"
    ),
    partial_update=extend_schema(
        description="Частичное изменение информации о команде",
        summary="Частичное изменение информации о команде"
    ),
    update=extend_schema(
        description="Изменение информации о команде",
        summary="Изменение информации о команде"
    ),
)
@extend_schema(tags=["team"])
class TeamViewSet(viewsets.ModelViewSet):
    """Представление для команд."""

    permission_classes = [IsSuperuserOrReadOnly, ]

    def get_queryset(self):
        queryset = Team.objects.annotate(
            employee_count=Count('gazpromuserteam__employee')
        )
        if self.action in ("retrieve", "list"):
            queryset = queryset.select_related(
                "team_manager",
                "product"
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TeamWriteSerializer
        elif self.action == "list":
            return TeamListSerializer
        elif self.action == "retrieve":
            return TeamGetSerializer
        elif self.action == "employees_list":
            return TeamEmployeeListSerializer
        elif self.action == "add_employees":
            return TeamAddEmployeesSerializer
        elif self.action == "remove_employees":
            return TeamDeleteEmployeesSerializer
        return TeamListSerializer

    @extend_schema(
        responses={
            200: TeamEmployeeListSerializer(many=True),
            404: OpenApiResponse(
                description="No Team matches the given query.",
            )
        },
        description="Получение списка сотрудников.",
        summary="Получение списка сотрудников."
    )
    @action(["get"], detail=True, url_path="employees_list")
    def employees_list(self, request, pk=None):
        """Получение списка сотрудников команды."""
        team = self.get_object()
        employees = GazpromUserTeam.objects.filter(team=team).select_related(
            "employee"
        )
        page = self.paginate_queryset(employees)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        request=TeamAddEmployeesSerializer,
        responses={
            200: TeamAddEmployeesSerializer,
            400: OpenApiResponse(
                description="Invalid data",
            )
        },
        description="Добавление сотрудников в команду.",
        summary="Добавление сотрудников в команду."
    )
    @action(["post"], detail=True, url_path="add_employees")
    def add_employees(self, request, pk=None):
        """Добавление сотрудников в команду."""
        team = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"team": team}
        )
        if serializer.is_valid():
            employee_ids = serializer.validated_data["employee_ids"]
            role = serializer.validated_data["role"]
            GazpromUserTeam.objects.bulk_create(
                [
                    GazpromUserTeam(
                        employee_id=employee_id,
                        team=team,
                        role=role,
                    )
                    for employee_id in employee_ids
                ]
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=TeamDeleteEmployeesSerializer,
        responses={
            204: TeamDeleteEmployeesSerializer,
            400: OpenApiResponse(
                description="Invalid data",
            )
        },
        description="Удаление сотрудников из команды.",
        summary="Удаление сотрудников из команды."
    )
    @action(["delete"], detail=True, url_path="remove_employees")
    def remove_employees(self, request, pk=None):
        """Удаление сотрудников из команды."""
        team = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data["employee_ids"]
            GazpromUserTeam.objects.filter(
                team=team,
                employee_id__in=employee_ids
            ).delete()
            return Response(
                serializer.data,
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
