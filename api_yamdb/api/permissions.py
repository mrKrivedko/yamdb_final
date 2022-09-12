from rest_framework import permissions


class OnlyAuthor(permissions.BasePermission):
    """Разрешение действий с обьектом только для автора."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return obj.author.username == request.user.username


class OnlyAuthorOrVIPRole(OnlyAuthor):
    """Разрешение действий с обьектом только для автора."""

    def has_object_permission(self, request, view, obj):
        """Разрешаем также если пользователь модератор или администратор"""
        return (
            obj.author == request.user
            or request.user.is_vip
        )


class VIProle(permissions.BasePermission):
    """Пермишн только для модератора или администратора."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_vip
            )
        )


class OnlyModerator(OnlyAuthor):
    """Разрешение действий с обьектом только для модератора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class OnlyAdmin(permissions.BasePermission):
    """Разрешение действий с обьектом только для администратора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class OnlyAdminOrReadonly(permissions.BasePermission):
    """Разрешение действий с обьектом только для администратора ."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrVIPRole(permissions.BasePermission):
    """Проверка на авторство, либо роли администратора/модератора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_anonymous
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_vip
                    or obj.author == request.user
                )
            )
        )
