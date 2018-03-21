from django.urls import path
from rest_framework import routers

from ticketingapp.views import MallViewSet, ParkingTicketViewSet, pay_ticket, exit_park

router = routers.SimpleRouter()
router.register('mall', MallViewSet)
router.register('parkingtickets', ParkingTicketViewSet)

urlpatterns = [
    path('parkingtickets/<int:ticket_id>/pay-ticket',
         pay_ticket, name="payment-route"),
    path('parkingtickets/<int:ticket_id>/exit', exit_park, name="exit-route")
]

urlpatterns += router.urls
