from django.contrib import admin
from django.contrib.auth import get_user_model

from company.admin import AdditionalFieldInline, MetricInline
from users.models import Skill

User = get_user_model()


class SkillsInline(admin.TabularInline):
    model = Skill.users.through
    extra = 0


class GazpromUserAdmin(admin.ModelAdmin):
    """Отображение пользователей."""

    list_display = ["id", "employee_fio"]
    fields = [
        "employee_fio",
        "email",
        "employee_position",
        "employee_date_of_birth",
        "employee_date_of_hire",
        "employee_avatar",
        "employee_telegram",
        "employee_telephone",
        "employee_type_job",
        "employee_status",
        "employee_location",
        "employee_grade",
        "employee_description",
        "is_employee_outsource",
        "employee_departament",
    ]
    inlines = [AdditionalFieldInline, MetricInline, SkillsInline]


admin.site.register(User, GazpromUserAdmin)
admin.site.register(Skill)
