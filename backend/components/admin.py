from django.contrib import admin

from company.admin import AdditionalFieldInline, MetricInline
from components.models import Component


class ComponentAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline]


admin.site.register(Component, ComponentAdmin)
