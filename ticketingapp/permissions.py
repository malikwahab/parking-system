from rest_framework import permissions
from ticketingapp.models import Park


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Filters that allow only park owner to see parkedcars
    """

    def has_permission(self, request, views):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user and
                request.user.is_staff
        )

    # def has_object_permission(self, request, views, obj):
    #     park = obj.park
    #     return super().has_object_permission(request, views, park)
