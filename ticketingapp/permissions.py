from rest_framework import permissions
from ticketingapp.models import Mall


class IsAdmin(permissions.BasePermission):
    """Ensure all allowed access is of the object owner."""

    def has_object_permission(self, request, views, obj):
        return obj.admin == request.user


class IsMallAdmin(IsAdmin):
    """Filters that allow only mall owner to see parkedcars
    """

    def has_permission(self, request, views):
        mall = Mall.objects.get(id=views.kwargs['mall_pk'])
        return super().has_object_permission(request, views, mall)

    def has_object_permission(self, request, views, obj):
        mall = obj.mall
        return super().has_object_permission(request, views, mall)
