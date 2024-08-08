from django.contrib import admin

from company.models import AdditionalField, Metric

admin.site.register(AdditionalField)
admin.site.register(Metric)
