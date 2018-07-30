from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters, mixins, permissions

from rest_framework_jwt.settings import api_settings as jwt_settings

from ticketingapp.models import ParkingTicket, Mall, Tenant
from ticketingapp.serializers import (
    ParkingTicketSerializer,
    MallSerializer,
    AdminMallSerializer,
    TenantSerializer,
    UserSerializer
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
    permission_classes = (IsAdmin,)
    filter_backends = (IsMallAdminFilterBackend, )


class AdminMallViewSet(ModelViewSet, PartialPutMixin):
    queryset = Mall.objects.all()
    serializer_class = AdminMallSerializer
    permission_classes = (permissions.IsAdminUser,)


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


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    """The API class for creating User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Generate api token
        jwt_payload_handler = jwt_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = jwt_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'user': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """To return the created user. """
        return serializer.save()



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
