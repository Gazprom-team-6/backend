from django.contrib import admin

from company.models import (AdditionalField, Component, Department,
                            GazpromUserTeam, Metric, Product, Team)

admin.site.register(Product)
admin.site.register(Component)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(GazpromUserTeam)
admin.site.register(AdditionalField)
admin.site.register(Metric)
