from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class AdditionalField(models.Model):
    """Модель для дополнительных полей."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Содержание поля")

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "Дополнительные поля"
        default_related_name = "additionalfield"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.name


class Metric(models.Model):
    """Модель метрик."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Содержание метрики")

    class Meta:
        verbose_name = "метрика"
        verbose_name_plural = "Метрики"
        default_related_name = "metric"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.name
