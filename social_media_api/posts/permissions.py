from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    """
    Read: allowed to anyone.
    Write: only owners (object.author == request.user).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
