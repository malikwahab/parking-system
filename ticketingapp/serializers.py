from rest_framework import serializers
from rest_framework.settings import api_settings

from ticketingapp.models import ParkingTicket, Mall


class ParkingTicketSerializer(serializers.ModelSerializer):
    
    # accumulated_ticket_fee
    ticket_fee = serializers.ReadOnlyField(source='amount_owed')

    url = serializers.HyperlinkedIdentityField(
        view_name='parkingticket-detail'
    )

    class Meta:
        model = ParkingTicket
        fields = ('plate_number', 'entry_time', 'date_modified',
                  'exit_time', 'fee_paid', 'status', 'mall', 'ticket_fee', 'url')
        read_only_fields = ('exit_time', 'fee_paid', 'status',)


class MallSerializer(serializers.ModelSerializer):

    parkingtickets = ParkingTicketSerializer(many=True, read_only=True)
    
    class Meta:
        model = Mall
        fields = ('name', 'maximum_no_cars', 'date_created', 'date_modified',
                  'parkingtickets', )
