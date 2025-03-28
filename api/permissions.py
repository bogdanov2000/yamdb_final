from rest_framework import permissions
from .models import UserRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == UserRole.ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == UserRole.ADMIN


class IsAuthorOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (
                request.user.is_staff
                or request.user.role in (UserRole.ADMIN, UserRole.MODERATOR)
                or obj.author == request.user
                or (request.method == "POST" and request.user.is_authenticated)
            ):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
