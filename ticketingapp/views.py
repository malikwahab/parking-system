from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, filters, mixins, permissions

from ticketingapp.models import ParkingTicket, Park, Tenant, TenantCars
from ticketingapp.serializers import (
    ParkingTicketSerializer,
    ParkSerializer,
    TenantSerializer,
    TenantCarSerializer
)
from ticketingapp.permissions import IsAdminUserOrReadOnly, IsTenantAdmin, CanCRUDTenantCar
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
    filter_fields = ("status", "plate_number",)  # use status to return only parked cars to users app
    search_fields = ('plate_number',)

    def perform_create(self, serializer):
        park = Park.objects.get(id=self.kwargs['park_pk'])
        serializer.save(park=park)

    def get_queryset(self):
        return ParkingTicket.objects.filter(park=self.kwargs['park_pk'])


class TenantViewSet(ModelViewSet, PartialPutMixin):
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()

    permission_classes = (permissions.DjangoModelPermissions, IsTenantAdmin)  # Permission controlled by Admin

    def get_queryset(self):
        tenants = super().get_queryset()
        if self.request.user.is_staff:
            return tenants
        return tenants.filter(admins__in=(self.request.user,))


class TenantCarViewSet(ModelViewSet, PartialPutMixin):
    serializer_class = TenantCarSerializer
    queryset = TenantCars.objects.all()
    permission_classes = (permissions.DjangoModelPermissions, CanCRUDTenantCar,)

    def perform_create(self, serializer):
        tenant = Tenant.objects.get(id=self.kwargs["tenant_pk"])
        serializer.save(tenant=tenant)

    def get_queryset(self):
        tenant_cars = super().get_queryset()
        if self.request.user.is_staff:
            return tenant_cars
        return tenant_cars.filter(tenant=self.kwargs["tenant_pk"])


# Views below were added just to use @api_view

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser,])
def check_out(request, ticket_id):
    """The view for checking out a ticket before paying."""
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    fee = parkingticket.checkout()
    serializer = ParkingTicketSerializer(
        parkingticket, context={'request': request})
    return Response({
        "fee": fee,
        "ticket": serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser,])
def pay_ticket(request, ticket_id):
    """
    This endpoint is to make payment for parking tickets
    You can also make partial payment
    """
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    parkingticket.checkout()
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
@permission_classes([permissions.IsAdminUser,])
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
