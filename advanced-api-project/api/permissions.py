from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permissions to allow full access to authenticated users and read-only access to unauthenticated users

    """
    def has_permission(self, request, view):
        # Read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write access for authenticated users
        return request.user and resquest.user.is_authenticated