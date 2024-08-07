import django_filters
from django.contrib.auth import get_user_model

from users.constants import GRADES, JOB_TYPES
from users.models import Skill

User = get_user_model()


class GazpromUserFilter(django_filters.FilterSet):
    """Фильтрация пользователей (сотрудников)."""

    position = django_filters.CharFilter(field_name="employee_position")
    department = django_filters.CharFilter(
        field_name="employee_departament__departament_name"
    )
    grade = django_filters.ChoiceFilter(
        field_name="employee_grade",
        choices=GRADES,
    )
    job_type = django_filters.ChoiceFilter(
        field_name="employee_type_job",
        choices=JOB_TYPES,
    )
    skill = django_filters.ModelMultipleChoiceFilter(
        field_name="skills__name",
        to_field_name="name",
        queryset=Skill.objects.all(),
    )
    is_outsource = django_filters.BooleanFilter(
        field_name="is_employee_outsource"
    )
    location = django_filters.CharFilter(field_name="employee_location")
    team = django_filters.CharFilter(
        field_name="gazpromuserteam__team__team_name"
    )
    product = django_filters.CharFilter(
        field_name="gazpromuserteam__team__product__product_name"
    )

    class Meta:
        model = User
        fields = ["position", "department", "grade", "skill",
                  "is_outsource", "is_outsource", "location", "team",
                  "product", "job_type"]
