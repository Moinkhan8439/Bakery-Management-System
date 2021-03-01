from rest_framework import permissions


class IsCustomer(permissions.BasePermission):

    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)