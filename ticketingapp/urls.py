from django.urls import path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from ticketingapp.views import (MallViewSet,
                                ParkingTicketViewSet,
                                TenantViewset,
                                pay_ticket,
                                exit_park,
                                payment_details)

router = routers.DefaultRouter()
router.register('mall', MallViewSet)

mall_router = NestedSimpleRouter(router, 'mall', lookup='mall')
mall_router.register('parkingtickets', ParkingTicketViewSet, base_name='mall-parkingtickets')
mall_router.register('tenants', TenantViewset, base_name='mall-tenants')

urlpatterns = [
    path('pay-ticket/<int:ticket_id>',
         pay_ticket, name="payment-route"),
    path('exit/<int:ticket_id>', exit_park, name='exit-route'),
    path('mall/<int:mall_id>/payment-details',
         payment_details, name='payment-details-route'),
    path('auth-users', obtain_jwt_token),

    *router.urls,
    *mall_router.urls
]
