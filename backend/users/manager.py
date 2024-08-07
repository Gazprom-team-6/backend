from django.contrib.auth.base_user import BaseUserManager


class GazpromUserManager(BaseUserManager):
    """
    Менеджер пользователей.
    Этот менеджер обеспечивает создание и управление пользователями в системе.
    """
    def create_user(self, email, password=None, **extra_fields):
        """Создание и сохранение обычного пользователя."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание и сохранение суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
