from django.contrib.contenttypes.models import ContentType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from company.models import AdditionalField, Metric
from company.schemas import (ADD_FIELD_SCHEMA, ADD_METRIC_SCHEMA,
                             GET_FIELDS_SCHEMA, GET_METRIC_SCHEMA)
from company.serializers import AdditionalFieldSerializer, MetricSerializer


class BaseViewSet(viewsets.ModelViewSet):
    """Миксин для всех сущностей с базовым набором actions"""

    def get_serializer_class(self):
        if self.action in ("add_field", "get_fields"):
            return AdditionalFieldSerializer
        else:
            return MetricSerializer

    def handle_additional_data(
            self,
            request,
            pk,
            serializer_class,
            model_class
    ):
        """Обработчик добавлеmodel_classния дополнительных данных."""
        model_object = self.get_object()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        description = serializer.validated_data["description"]
        additional_data = model_class(
            content_object=model_object, name=name, description=description
        )
        additional_data.save()
        return Response(
            serializer_class(additional_data).data, status=status.HTTP_200_OK
        )

    @ADD_FIELD_SCHEMA
    @action(methods=["post"], detail=True, url_path="add_field")
    def add_field(self, request, pk=None):
        """Добавление дополнительного поля."""
        return self.handle_additional_data(
            request,
            pk,
            serializer_class=AdditionalFieldSerializer,
            model_class=AdditionalField,
        )

    @ADD_METRIC_SCHEMA
    @action(methods=["post"], detail=True, url_path="add_metric")
    def add_metric(self, request, pk=None):
        """Добавление метрики."""
        return self.handle_additional_data(
            request, pk, serializer_class=MetricSerializer, model_class=Metric
        )

    def get_additional_data(self, request, pk, model):
        """
        Метод для получения списка связанных метрик и дополнительных полей.
        """
        model_object = self.get_object()
        # Фильтрация по связанному объекту
        metrics = model.objects.filter(
            content_type=ContentType.objects.get_for_model(model_object),
            object_id=model_object.id
        )
        return self.get_paginated_data(request=request, queryset=metrics)

    @GET_FIELDS_SCHEMA
    @action(methods=["get"], detail=True, url_path="get_fields")
    def get_fields(self, request, pk=None):
        """Получение списка дополнительных полей."""
        return self.get_additional_data(
            request=request,
            pk=pk,
            model=AdditionalField
        )

    @GET_METRIC_SCHEMA
    @action(methods=["get"], detail=True, url_path="get_metrics")
    def get_metrics(self, request, pk=None):
        """Получение списка метрик."""
        return self.get_additional_data(request=request, pk=pk, model=Metric)

    def get_paginated_data(self, request, queryset):
        """Пагинация и сериализия queryset."""
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def is_object_exists(self, pk):
        """Проверка, существует ли объект в БД."""
        if not self.get_queryset().filter(id=pk).exists():
            return Response(
                {"detail": "No Objects matches the given query."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return None
