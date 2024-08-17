from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.mail import send_mail


@shared_task(base=Singleton)
def send_reset_password_email(new_password, email):
    """Отправка email для восстановления пароля."""
    send_mail(
        subject="Восстановление пароля",
        message=f"Ваш новый пароль: {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task(base=Singleton)
def send_add_to_team_mail(team_name, emails):
    """Отправка email с уведомлением об удалении сотрудника из команды."""
    send_mail(
        subject=f"Вас добавили в команду {team_name}",
        message=f"Вас добавили в команду {team_name}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )


@shared_task(base=Singleton)
def send_remove_from_team_mail(team_name, emails):
    """Отправка email с уведомлением об удалении сотрудника из команды."""
    send_mail(
        subject=f"Вас исключили из команды {team_name}",
        message=f"Вас исключили из команды {team_name}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )
