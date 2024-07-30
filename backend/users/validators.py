from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r'^\+\d{10,15}$',
        message=_(
            "Phone number must start with '+' and contain 10 to 15 digits."
        )
    )


def validate_birth_date(value):
    """Валидация даты рождения."""
    if value > date.today():
        raise ValidationError("Дата рождения не может быть в будущем.")
    if value.year < 1900:
        raise ValidationError("Год рождения не может быть меньше 1900.")