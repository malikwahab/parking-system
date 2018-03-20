from rest_framework import serializers
from ticketingapp.models import ParkingTicket, Mall


class ParkingTicketSerializer(serializers.ModelSerializer):

    # TODO: Change to hyperfield after view is created
    # mall = serializers.ReadOnlyField(source='mall.name')

    class Meta:
        model = ParkingTicket
        fields = ('id', 'plate_number', 'entry_time', 'exit_time', 'fee_paid',
                  'date_modified', 'mall',)


class MallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mall
        fields = ('name', 'maximum_no_cars', 'date_created', 'date_modified',)

