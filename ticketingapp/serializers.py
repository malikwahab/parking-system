from rest_framework import serializers

from ticketingapp.models import ParkingTicket, Park, Tenant, TenantCars


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
    available_space = serializers.ReadOnlyField()
    total_amount_paid = serializers.ReadOnlyField(source="get_amount_paid")
    total_amount_owned = serializers.ReadOnlyField(source="get_amount_owned")
    number_of_parked_cars = serializers.ReadOnlyField()

    class Meta:
        model = Park
        fields = '__all__'
        read_only_fields = ('tenants',)


class TenantCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantCars
        fields = '__all__'
        extra_kwargs = {'tenant': {'required': False}}


class TenantSerializer(serializers.ModelSerializer):
    cars = TenantCarSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = '__all__'
