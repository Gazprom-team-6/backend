from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from company.models import AdditionalField, Metric
from company.schemas import ADD_FIELD_SCHEMA, ADD_METRIC_SCHEMA
from company.serializers import AdditionalFieldSerializer, MetricSerializer


class BaseViewSet(viewsets.ModelViewSet):
    """Миксин для всех сущностей с базовым набором actions"""

    def get_serializer_class(self):
        if self.action == "add_field":
            return AdditionalFieldSerializer
        elif self.action == "add_metric":
            return MetricSerializer
        return super().get_serializer_class()

    def handle_additional_data(
            self,
            request,
            pk,
            serializer_class,
            model_class
    ):
        """Обработчик добавления дополнительных данных."""
        model_object = self.get_object()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            additional_data = model_class(
                content_object=model_object,
                name=name,
                description=description
            )
            additional_data.save()
            return Response(
                serializer_class(additional_data).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @ADD_FIELD_SCHEMA
    @action(methods=["post"], detail=True, url_path="add_field")
    def add_field(self, request, pk=None):
        """Добавление дополнительного поля."""
        return self.handle_additional_data(
            request,
            pk,
            serializer_class=AdditionalFieldSerializer,
            model_class=AdditionalField
        )

    @ADD_METRIC_SCHEMA
    @action(methods=["post"], detail=True, url_path="add_metric")
    def add_metric(self, request, pk=None):
        """Добавление метрики."""
        return self.handle_additional_data(
            request,
            pk,
            serializer_class=MetricSerializer,
            model_class=Metric
        )
