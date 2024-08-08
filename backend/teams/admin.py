from django.contrib import admin

from company.admin import AdditionalFieldInline, MetricInline
from teams.models import Team


class TeamAdmin(admin.ModelAdmin):
    inlines = [AdditionalFieldInline, MetricInline]


admin.site.register(Team, TeamAdmin)
