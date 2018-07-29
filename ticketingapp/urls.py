from django.urls import path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from ticketingapp.views import (MallViewSet,
                                AdminMallViewSet,
                                ParkingTicketViewSet,
                                TenantViewset,
                                UserViewSet,
                                pay_ticket,
                                exit_park,
                                payment_details)

router = routers.DefaultRouter()
router.register('mall', MallViewSet)
router.register('admin-mall', AdminMallViewSet, base_name="admin-mall")
router.register('users', UserViewSet)

mall_router = NestedSimpleRouter(router, 'mall', lookup='mall')
mall_router.register('parkingtickets', ParkingTicketViewSet, base_name='mall-parkingtickets')
mall_router.register('tenants', TenantViewset, base_name='mall-tenants')

urlpatterns = [
    path('pay-ticket/<int:ticket_id>',
         pay_ticket, name="payment-route"),
    path('exit/<int:ticket_id>', exit_park, name='exit-route'),
    path('mall/<int:mall_id>/payment-details',
         payment_details, name='payment-details-route'),
]

urlpatterns += [*router.urls, *mall_router.urls]
