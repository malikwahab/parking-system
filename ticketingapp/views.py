from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters, mixins, permissions

from ticketingapp.models import ParkingTicket, Mall, Tenant
from ticketingapp.serializers import (
    ParkingTicketSerializer,
    MallSerializer,
    TenantSerializer
)
from ticketingapp.filters import IsMallAdminFilterBackend
from ticketingapp.permissions import IsMallAdmin, IsAdmin
# Create your views here.


class PartialPutMixin(mixins.UpdateModelMixin):
    # force PUT to be a partial update
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class MallViewSet(mixins.RetrieveModelMixin,
                   PartialPutMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    This endpoint presents the malls in the System
    """
    serializer_class = MallSerializer
    queryset = Mall.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    filter_backends = (IsMallAdminFilterBackend, )


class ParkingTicketViewSet(ModelViewSet, PartialPutMixin):
    serializer_class = ParkingTicketSerializer
    queryset = ParkingTicket.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    permission_classes = (IsMallAdmin,)
    filter_fields = ('status',)
    search_fields = ('plate_number',)

    def perform_create(self, serializer):
        mall = Mall.objects.get(id=self.kwargs['mall_pk'])
        serializer.save(mall=mall)

    def get_queryset(self):
        return ParkingTicket.objects.filter(mall=self.kwargs['mall_pk'])


class TenantViewset(ModelViewSet, PartialPutMixin):
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()


@api_view(['POST'])
def pay_ticket(request, ticket_id):
    """
    This endpoint is to make payment for parking tickets
    You can also make partial payment
    """
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    parkingticket.checkout()  # TODO: refactor checkout logic
    fee_paid = float(request.data['fee_paid'])
    parkingticket.pay_ticket(fee_paid)
    serializer = ParkingTicketSerializer(
        parkingticket, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def exit_park(request, ticket_id):
    """
    This endpoint is to exit the park. Throws error if there
    is outstanding payment on the ticket
    """
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    if parkingticket.exit_park():
        serializer = ParkingTicketSerializer(
            parkingticket, context={'request': request})
        return Response(serializer.data)
    return Response({'message': 'Outstanding payment, can\'t exit park'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def payment_details(request, mall_id):
    """
    This endpoint presents the payment information on a mall. It accepts
    query param "days" to limit the calculated fee to since days specified
    """
    mall = get_object_or_404(Mall, pk=mall_id)
    serializer = MallSerializer(mall, context={'request': request})
    days = request.query_params.get('days', [None])[0]
    return Response({
        'paid': mall.get_amount_paid(days),
        'owned': mall.get_amount_owned(days),
        'mall': serializer.data
    })
