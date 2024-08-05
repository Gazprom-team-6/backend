from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """Разрешаем доступ для редактирования только суперпользователю."""

    def has_permission(self, request, view):
        # Разрешаем безопасные методы для аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Разрешаем все действия суперпользователю
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы для аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Разрешаем все действия суперпользователю
        return request.user and request.user.is_superuser
