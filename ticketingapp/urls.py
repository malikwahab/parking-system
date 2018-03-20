from django.urls import path
from rest_framework import routers

from ticketingapp.views import MallViewSet, ParkingTicketViewSet

router = routers.SimpleRouter()
router.register('mall', MallViewSet)
router.register('parkingtickets', ParkingTicketViewSet)

urlpatterns = router.urls
