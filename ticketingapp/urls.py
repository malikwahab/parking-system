from django.urls import path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from ticketingapp.views import (MallViewSet,
                                ParkingTicketViewSet,
                                MallParkingTicketViewSet,
                                pay_ticket,
                                exit_park,
                                payment_details)

router = routers.DefaultRouter()
router.register('mall', MallViewSet)
router.register('parkingtickets', ParkingTicketViewSet)

mall_router = NestedSimpleRouter(router, 'mall', lookup='mall')
mall_router.register('parkingtickets', MallParkingTicketViewSet, base_name='mall-parkingtickets')

urlpatterns = [
    path('parkingtickets/<int:ticket_id>/pay-ticket',
         pay_ticket, name="payment-route"),
    path('parkingtickets/<int:ticket_id>/exit', exit_park, name='exit-route'),
    path('mall/<int:mall_id>/payment-details',
         payment_details, name='payment-details-route')
]

urlpatterns += [*router.urls, *mall_router.urls]
