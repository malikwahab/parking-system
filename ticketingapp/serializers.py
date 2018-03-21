from rest_framework import serializers
from ticketingapp.models import ParkingTicket, Mall


class ParkingTicketSerializer(serializers.ModelSerializer):

    # TODO: Change to hyperfield after view is created
    # mall = serializers.CharField(source='mall.name')
    
    # accumulated_ticket_fee
    ticket_fee = serializers.ReadOnlyField(source='amount_owed')

    class Meta:
        model = ParkingTicket
        fields = ('id', 'plate_number', 'entry_time', 'date_modified',
                  'exit_time', 'fee_paid', 'status', 'mall', 'ticket_fee',)
        read_only_fields = ('exit_time', 'fee_paid', 'status',)


class MallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mall
        fields = ('name', 'maximum_no_cars', 'date_created', 'date_modified',)
