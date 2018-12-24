from rest_framework import permissions
from ticketingapp.models import Park


class IsAdmin(permissions.BasePermission):
    """Ensure all allowed access is of the object owner."""

    def has_object_permission(self, request, views, obj):
        return obj.admin == request.user


class IsParkAdmin(IsAdmin):
    """Filters that allow only park owner to see parkedcars
    """

    def has_permission(self, request, views):
        park = Park.objects.get(id=views.kwargs['park_pk'])
        return super().has_object_permission(request, views, park)

    def has_object_permission(self, request, views, obj):
        park = obj.park
        return super().has_object_permission(request, views, park)
