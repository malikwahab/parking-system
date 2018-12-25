from rest_framework import permissions
from ticketingapp.models import Tenant, TenantCars


class IsTenantAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user in obj.admins.all()


class CanCRUDTenantCar(IsTenantAdmin):

    def has_permission(self, request, view):
        tenant = Tenant.objects.get(id=view.kwargs["tenant_pk"])
        return super().has_object_permission(request, view, tenant)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Filters that allow only park owner to see parkedcars
    """

    def has_permission(self, request, views):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user and
                request.user.is_staff
        )
