from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r'^\+\d{10,15}$',
        message="Номер телефона должен начинаться с + и состоять из 10-15 цифр"
    )


def validate_birth_date(value):
    """Валидация даты рождения."""
    if value > date.today():
        raise ValidationError("Дата рождения не может быть в будущем.")
    if value.year < 1900:
        raise ValidationError("Год рождения не может быть меньше 1900.")


def validate_hire_date(value):
    """Валидация даты найма."""
    if value > date.today():
        raise ValidationError("Дата найма не может быть в будущем.")
    if value.year < 1989:
        raise ValidationError("Год найма не может быть раньше "
                              "года основания компании (1989).")
