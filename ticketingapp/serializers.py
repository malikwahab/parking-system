from rest_framework import serializers
from rest_framework.settings import api_settings

from ticketingapp.models import ParkingTicket, Mall


class ParkingTicketSerializer(serializers.ModelSerializer):
    # accumulated_ticket_fee
    ticket_fee = serializers.ReadOnlyField(source='amount_owed')

    url = serializers.HyperlinkedIdentityField(
        view_name='parkingticket-detail'
    )

    def create(self, validated_data):
        mall = validated_data['mall']
        if mall.is_parked(validated_data['plate_number']):
            raise serializers.ValidationError('This car is already parked!')
        if not mall.has_space():
            raise serializers.ValidationError('Mall Park is filled!')
        return super().create(validated_data)

    class Meta:
        model = ParkingTicket
        fields = ('plate_number', 'entry_time', 'date_modified',
                  'exit_time', 'fee_paid', 'status', 'mall', 'ticket_fee',
                  'url')
        read_only_fields = ('exit_time', 'fee_paid', 'status',)


class MallSerializer(serializers.ModelSerializer):
    parkingtickets_url = serializers.HyperlinkedIdentityField(
        view_name='mall-parkingtickets-list',
        lookup_field='pk',
        lookup_url_kwarg='mall_pk'
    )

    class Meta:
        model = Mall
        fields = ('name', 'maximum_no_cars', 'date_created', 'date_modified',
                  'parkingtickets_url',)
