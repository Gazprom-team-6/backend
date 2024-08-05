from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Skill

User = get_user_model()


class GazpromUserAdmin(admin.ModelAdmin):
    """Отображение пользователей."""

    list_display = ["id", "employee_fio"]
    fields = ["employee_fio", "email", "employee_position",
              "employee_date_of_birth", "employee_date_of_hire",
              "employee_avatar", "employee_telegram", "employee_telephone",
              "employee_type_job", "employee_status", "employee_location",
              "employee_grade", "employee_description",
              "is_employee_outsource", "skills", "employee_departament"]


admin.site.register(User, GazpromUserAdmin)
admin.site.register(Skill)
