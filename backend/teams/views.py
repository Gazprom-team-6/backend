from django.db.models import Count
from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from company.permissions import IsSuperuserOrReadOnly
from teams.models import GazpromUserTeam, Team
from teams.serializers import (TeamAddEmployeesSerializer,
                               TeamDeleteEmployeesSerializer,
                               TeamEmployeeListSerializer, TeamGetSerializer,
                               TeamListSerializer, TeamWriteSerializer)


# Create your views here.
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
