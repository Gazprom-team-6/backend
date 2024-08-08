from django.contrib import admin

from company.admin import AdditionalFieldInline, MetricInline
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline]


admin.site.register(Product, ProductAdmin)
