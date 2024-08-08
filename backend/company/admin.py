from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from company.models import AdditionalField, Metric


class AdditionalFieldInline(GenericTabularInline):
    """Добавляем дополнительные поля в админку."""
    model = AdditionalField
    extra = 1


class MetricInline(GenericTabularInline):
    """Добавляем дополнительные метрики в админку."""
    model = Metric
    extra = 1


admin.site.register(AdditionalField)
admin.site.register(Metric)
