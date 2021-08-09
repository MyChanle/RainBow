""" permissions.py """

from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """ IsAdminUserOrReadOnly """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
    
        return request.user.is_superuser
