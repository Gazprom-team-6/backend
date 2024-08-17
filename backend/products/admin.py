from django.contrib import admin

from company.admin import AdditionalFieldInline, MetricInline
from components.models import Component
from products.models import Product


class ComponentInline(admin.TabularInline):
    model = Component.product.through
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline, ComponentInline]
    filter_horizontal = ("components",)


admin.site.register(Product, ProductAdmin)
