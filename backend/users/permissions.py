from rest_framework import permissions


class IsSuperuser(permissions.IsAuthenticated):
    """Разрешаем доступ к объекту только суперпользователю."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsSuperuserOrProfileOwner(permissions.IsAuthenticated):
    """
    Разрешаем доступ к объекту только суперпользователю и владельцу
    объекта.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user

