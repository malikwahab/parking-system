from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters, mixins, permissions

from ticketingapp.models import ParkingTicket, Park, Tenant
from ticketingapp.serializers import (
    ParkingTicketSerializer,
    ParkSerializer,
    TenantSerializer
)
from ticketingapp.permissions import IsAdminUserOrReadOnly
# Create your views here.


class PartialPutMixin(mixins.UpdateModelMixin):
    # force PUT to be a partial update
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ParkViewSet(ModelViewSet, PartialPutMixin):
    """
    This endpoint presents the parks in the System
    """
    serializer_class = ParkSerializer
    queryset = Park.objects.all()
    permission_classes = (permissions.DjangoModelPermissions, )  # Permission controlled by Admin


class ParkingTicketViewSet(ModelViewSet, PartialPutMixin):
    serializer_class = ParkingTicketSerializer
    queryset = ParkingTicket.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_fields = ('status',)
    search_fields = ('plate_number',)

    def perform_create(self, serializer):
        park = Park.objects.get(id=self.kwargs['park_pk'])
        serializer.save(park=park)

    def get_queryset(self):
        return ParkingTicket.objects.filter(park=self.kwargs['park_pk'])


class TenantViewset(ModelViewSet, PartialPutMixin):
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()

    permission_classes = (permissions.DjangoModelPermissions,)  # Permission controlled by Admin


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
def payment_details(request, park_id):
    """
    This endpoint presents the payment information on a park. It accepts
    query param "days" to limit the calculated fee to since days specified
    """
    park = get_object_or_404(Park, pk=park_id)
    serializer = ParkSerializer(park, context={'request': request})
    days = request.query_params.get('days', [None])[0]
    return Response({
        'paid': park.get_amount_paid(days),
        'owned': park.get_amount_owned(days),
        'park': serializer.data
    })
