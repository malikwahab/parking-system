from rest_framework import serializers
from rest_framework.settings import api_settings

from ticketingapp.models import ParkingTicket, Mall, Tenant


class ParkingTicketSerializer(serializers.ModelSerializer):
    # accumulated_ticket_fee
    ticket_fee = serializers.ReadOnlyField(source='amount_owed')

    url = serializers.HyperlinkedIdentityField(
        view_name='parkingticket-detail'
    )

    def create(self, validated_data):
        mall = validated_data.get('mall')
        tenant = validated_data.get('tenant')
        if mall.is_parked(validated_data['plate_number']):
            raise serializers.ValidationError('This car is already parked!')
        if not mall.has_space():
            raise serializers.ValidationError('Mall Park is filled!')
        if tenant and tenant not in mall.tenants.all():
            raise serializers.ValidationError('Selected tenant not in mall')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        mall = validated_data['mall']
        tenant = validated_data.get('tenant')
        if tenant and tenant not in mall.tenants.all():
            raise serializers.ValidationError('Selected tenant not in mall')
        return super().update(instance, validated_data)

    class Meta:
        model = ParkingTicket
        fields = ('plate_number', 'entry_time', 'date_modified',
                  'exit_time', 'fee_paid', 'status', 'mall', 'ticket_fee',
                  'url', 'tenant',)
        read_only_fields = ('exit_time', 'fee_paid', 'status',)


class MallSerializer(serializers.HyperlinkedModelSerializer):
    parkingtickets_url = serializers.HyperlinkedIdentityField(
        view_name='mall-parkingtickets-list',
        lookup_field='pk',
        lookup_url_kwarg='mall_pk'
    )

    class Meta:
        model = Mall
        fields = ('name', 'maximum_no_cars', 'date_created', 'date_modified',
                  'parkingtickets_url', 'number_of_parked_cars', 'tenants',)


class TenantSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tenant
        fields = '__all__'
