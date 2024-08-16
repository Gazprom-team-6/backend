from celery import shared_task
from celery_singleton import Singleton
from django.core.mail import send_mail


@shared_task(base=Singleton)
def send_reset_password_email(new_password, email):
    """Отправка email для восстановления пароля."""
    send_mail(
        "Восстановление пароля",
        f"Ваш новый пароль: {new_password}",
        "sir.petri-petrov@yandex.ru",
        [email],
        fail_silently=False,
    )

@shared_task(base=Singleton)
def send_add_to_team_mail(team_name, role, email):
    """Отправка email с уведомлением о добавлении сотрудника в команду."""
    send_mail(
        f"Вас добавили в команду {team_name}",
        f"Вас добавили в команду {team_name}. "
        f"Ваша роль в команде: {role}",
        "sir.petri-petrov@yandex.ru",
        [email],
        fail_silently=False,
    )


@shared_task(base=Singleton)
def send_remove_from_team_mail(team_name, email):
    """Отправка email с уведомлением об удалении сотрудника из команды."""
    send_mail(
        f"Вас исключили из команды {team_name}",
        f"Вас исключили из команды {team_name}. ",
        "sir.petri-petrov@yandex.ru",
        [email],
        fail_silently=False,
    )
