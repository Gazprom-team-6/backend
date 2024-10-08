from functools import partial

from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from company.mixins import BaseViewSet
from company.permissions import IsSuperuserOrReadOnly
from teams.models import GazpromUserTeam, Team
from teams.schemas import (ADD_EMPLOYEES_SCHEMA, CHANGE_EMPLOYEE_ROLE_SCHEMA,
                           EMPLOYEES_LIST_SCHEMA, REMOVE_EMPLOYEES_SCHEMA,
                           TEAM_SCHEMA)
from teams.serializers import (TeamAddEmployeesSerializer,
                               TeamDeleteEmployeesSerializer,
                               TeamEmployeeChangeRoleSerializer,
                               TeamEmployeeListSerializer, TeamGetSerializer,
                               TeamListSerializer, TeamWriteSerializer)
from users.models import GazpromUser
from users.tasks import send_add_to_team_mail, send_remove_from_team_mail


@TEAM_SCHEMA
@extend_schema(tags=["team"])
class TeamViewSet(BaseViewSet):
    """Представление для команд."""

    permission_classes = [
        IsSuperuserOrReadOnly,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id", "team_name")

    def get_queryset(self):
        queryset = Team.objects.all()

        if self.action in ("retrieve", "list"):
            queryset = queryset.annotate(
                employee_count=Count("gazpromuserteam__employee")
            ).select_related(
                "team_manager",
            )
            common_fields = [
                "id",
                "team_name",
                "team_manager__id",
                "team_manager__employee_fio",
                "team_manager__employee_avatar",
                "team_manager__employee_position",
                "team_manager__employee_grade",
            ]
            if self.action == "list":
                queryset = queryset.only(
                    *common_fields,
                    "product",
                )
            else:
                queryset = queryset.select_related("product").only(
                    *common_fields,
                    "product__id",
                    "product__product_name",
                    "product__product_manager",
                    "product__product_description",
                    "product__parent_product",
                )
        return queryset

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return TeamWriteSerializer
            case "list":
                return TeamListSerializer
            case "retrieve":
                return TeamGetSerializer
            case "employees_list":
                return TeamEmployeeListSerializer
            case "add_employees":
                return TeamAddEmployeesSerializer
            case "remove_employees":
                return TeamDeleteEmployeesSerializer
            case "change_employee_role":
                return TeamEmployeeChangeRoleSerializer
            case _:
                return super().get_serializer_class()

    @EMPLOYEES_LIST_SCHEMA
    @action(["get"], detail=True, url_path="employees_list")
    def employees_list(self, request, pk=None):
        """Получение списка сотрудников команды."""
        team = self.get_object()
        employees = (
            GazpromUserTeam.objects.filter(team=team)
            .select_related("employee")
            .only(
                "role",
                "employee__id",
                "employee__employee_fio",
                "employee__employee_avatar",
                "employee__employee_position",
                "employee__employee_grade",
            )
        )
        return self.get_paginated_data(request=request, queryset=employees)

    @ADD_EMPLOYEES_SCHEMA
    @transaction.atomic
    @action(["post"], detail=True, url_path="add_employees")
    def add_employees(self, request, pk=None):
        """Добавление сотрудников в команду."""
        team = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"team": team}
        )
        serializer.is_valid(raise_exception=True)
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

        # Получаем список email всех сотрудников, добавляемых в команду
        emails = list(
            GazpromUser.objects.filter(id__in=employee_ids).values_list(
                "email", flat=True
            )
        )
        # Отправка уведомлений после успешного завершения транзакции
        transaction.on_commit(
            partial(
                send_add_to_team_mail.delay,
                team_name=team.team_name,
                emails=emails
            )
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @REMOVE_EMPLOYEES_SCHEMA
    @transaction.atomic
    @action(["patch"], detail=True, url_path="remove_employees")
    def remove_employees(self, request, pk=None):
        """Удаление сотрудников из команды."""
        team = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"team": team}
        )
        serializer.is_valid(raise_exception=True)
        employee_ids = serializer.validated_data["employee_ids"]

        GazpromUserTeam.objects.filter(
            team=team,
            employee_id__in=employee_ids
        ).delete()

        # Получаем список email всех сотрудников, удаляемых из команды
        emails = list(
            GazpromUser.objects.filter(id__in=employee_ids).values_list(
                "email", flat=True
            )
        )
        # Отправка уведомлений после успешного завершения транзакции
        transaction.on_commit(
            partial(
                send_remove_from_team_mail.delay,
                team_name=team.team_name,
                emails=emails,
            )
        )

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @CHANGE_EMPLOYEE_ROLE_SCHEMA
    @action(["patch"], detail=True, url_path="change_employee_role")
    def change_employee_role(self, request, pk=None):
        """Изменение роли пользователя в команде."""
        team = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"team": team}
        )
        serializer.is_valid(raise_exception=True)
        employee = serializer.validated_data["employee"]
        role = serializer.validated_data["role"]
        gazpromuserteam = get_object_or_404(
            GazpromUserTeam,
            team=team,
            employee=employee,
        )
        gazpromuserteam.role = role
        gazpromuserteam.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
