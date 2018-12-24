from django.urls import path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from ticketingapp.views import (ParkViewSet,
                                ParkingTicketViewSet,
                                TenantViewset,
                                pay_ticket,
                                exit_park,
                                payment_details)

router = routers.DefaultRouter()
router.register('park', ParkViewSet)

park_router = NestedSimpleRouter(router, 'park', lookup='park')
park_router.register('parkingtickets', ParkingTicketViewSet, base_name='park-parkingtickets')
park_router.register('tenants', TenantViewset, base_name='park-tenants')

urlpatterns = [
    path('pay-ticket/<int:ticket_id>',
         pay_ticket, name="payment-route"),
    path('exit/<int:ticket_id>', exit_park, name='exit-route'),
    path('park/<int:park_id>/payment-details',
         payment_details, name='payment-details-route'),
    path('auth-users', obtain_jwt_token),

    *router.urls,
    *park_router.urls
]
