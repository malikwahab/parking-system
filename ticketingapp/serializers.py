from rest_framework import serializers

from ticketingapp.models import ParkingTicket, Park, Tenant


class ParkingTicketSerializer(serializers.ModelSerializer):
    # accumulated_ticket_fee
    ticket_fee = serializers.ReadOnlyField(source='amount_owed')

    def create(self, validated_data):
        park = validated_data.get('park')
        tenant = validated_data.get('tenant')
        if park.is_parked(validated_data['plate_number']):
            raise serializers.ValidationError('This car is already parked!')
        if not park.has_space():
            raise serializers.ValidationError('Mall Park is filled!')
        if tenant and tenant not in park.tenants.all():
            raise serializers.ValidationError('Selected tenant not in park')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        park = validated_data.get('park')
        tenant = validated_data.get('tenant')
        if tenant and tenant not in park.tenants.all():
            raise serializers.ValidationError('Selected tenant not in park')
        return super().update(instance, validated_data)

    class Meta:
        model = ParkingTicket
        fields = ('id', 'plate_number', 'entry_time', 'date_modified',
                  'exit_time', 'fee_paid', 'status', 'park', 'ticket_fee', 'tenant',)
        read_only_fields = ('exit_time', 'fee_paid', 'status', 'park',)
        extra_kwargs = {'park': {'allow_empty': True, 'required': False}}


class ParkSerializer(serializers.ModelSerializer):
    parkingtickets_url = serializers.HyperlinkedIdentityField(
        view_name='park-parkingtickets-list',
        lookup_field='pk',
        lookup_url_kwarg='park_pk'
    )

    # Todo: Add available space to the serializer

    class Meta:
        model = Park
        fields = ('id', 'name', 'maximum_no_cars', 'date_created', 'date_modified',
                  'parkingtickets_url', 'number_of_parked_cars', 'tenants',)
        read_only_fields = ('tenants',)


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = '__all__'
