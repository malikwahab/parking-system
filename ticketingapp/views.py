from rest_framework.viewsets import ModelViewSet

from ticketingapp.models import ParkingTicket, Mall
from ticketingapp.serializers import ParkingTicketSerializer, MallSerializer

# Create your views here.


class MallViewSet(ModelViewSet):
    
    serializer_class = MallSerializer
    queryset = Mall.objects.all()


class ParkingTicketViewSet(ModelViewSet):

    serializer_class = ParkingTicketSerializer
    queryset = ParkingTicket.objects.all()
        