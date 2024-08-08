from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from company.models import AdditionalField, Metric
from departments.models import Department


class AdditionalFieldInline(GenericTabularInline):
    """Добавляем дополнительные поля в админку."""
    model = AdditionalField
    extra = 1


class MetricInline(GenericTabularInline):
    """Добавляем дополнительные метрики в админку."""
    model = Metric
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline]


admin.site.register(Department, DepartmentAdmin)