from drf_spectacular.utils import extend_schema

from company.serializers import AdditionalFieldSerializer, MetricSerializer

ADD_FIELD_SCHEMA = extend_schema(
    request=AdditionalFieldSerializer,
    responses={200: AdditionalFieldSerializer},
    description="Добавление дополнительного поля.",
    summary="Добавление дополнительного поля.",
)

ADD_METRIC_SCHEMA = extend_schema(
    request=MetricSerializer,
    responses={200: MetricSerializer},
    description="Добавление метрики.",
    summary="Добавление метрики.",
)

GET_METRIC_SCHEMA = extend_schema(
    responses={200: MetricSerializer(many=True)},
    description="Получение списка метрик.",
    summary="Получение списка метрик.",
)

GET_FIELDS_SCHEMA = extend_schema(
    responses={200: AdditionalFieldSerializer(many=True)},
    description="Получение списка дополнительных полей.",
    summary="Получение списка дополнительных полей.",
)
