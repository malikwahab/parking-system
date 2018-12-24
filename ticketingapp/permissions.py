from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Filters that allow only park owner to see parkedcars
    """

    def has_permission(self, request, views):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user and
                request.user.is_staff
        )
