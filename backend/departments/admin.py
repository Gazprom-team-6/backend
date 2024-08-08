from django.contrib import admin

from company.admin import AdditionalFieldInline, MetricInline
from departments.models import Department


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline]


admin.site.register(Department, DepartmentAdmin)
