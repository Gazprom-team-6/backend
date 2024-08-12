from django.db.models import Count
from drf_spectacular.utils import (extend_schema)
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from company.mixins import BaseViewSet
from company.permissions import IsSuperuserOrReadOnly
from teams.models import GazpromUserTeam, Team
from teams.schemas import (ADD_EMPLOYEES_SCHEMA, EMPLOYEES_LIST_SCHEMA,
                           REMOVE_EMPLOYEES_SCHEMA,
                           TEAM_SCHEMA)
from teams.serializers import (TeamAddEmployeesSerializer,
                               TeamDeleteEmployeesSerializer,
                               TeamEmployeeListSerializer, TeamGetSerializer,
                               TeamListSerializer, TeamWriteSerializer)


@TEAM_SCHEMA
@extend_schema(tags=["team"])
class TeamViewSet(BaseViewSet):
    """Представление для команд."""

    permission_classes = [IsSuperuserOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "team_name")

    def get_queryset(self):
        queryset = Team.objects.all()
        if self.action in ("retrieve", "list"):
            queryset = queryset.annotate(
                employee_count=Count('gazpromuserteam__employee')
            ).select_related(
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
        elif self.action == "list":
            return TeamListSerializer
        return super().get_serializer_class()

    @EMPLOYEES_LIST_SCHEMA
    # @method_decorator(cache_page(60 * 60 * 2))
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

    @ADD_EMPLOYEES_SCHEMA
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

    @REMOVE_EMPLOYEES_SCHEMA
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
