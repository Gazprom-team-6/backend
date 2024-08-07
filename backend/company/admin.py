from django.contrib import admin

from company.models import AdditionalField, Metric
from components.models import Component
from departments.models import Department
from products.models import Product
from teams.models import GazpromUserTeam, Team

admin.site.register(Product)
admin.site.register(Component)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(GazpromUserTeam)
admin.site.register(AdditionalField)
admin.site.register(Metric)
