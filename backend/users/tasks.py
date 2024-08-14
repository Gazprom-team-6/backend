from celery import shared_task
from celery_singleton import Singleton
from django.core.mail import send_mail


@shared_task(base=Singleton)
def send_reset_password_email(new_password, email):
    send_mail(
        "Восстановление пароля",
        f"Ваш новый пароль: {new_password}",
        "sir.petri-petrov@yandex.ru",
        [email],
        fail_silently=False,
    )
