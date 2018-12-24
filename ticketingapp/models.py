import math
import functools
from datetime import timedelta

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

plate_number_validator = RegexValidator("([A-Za-z]{3}\-\d{3}[A-Za-z]{2})", "Plate Number are in the format ABC-123DE")
STATUS = [('parked', 'parked'), ('exited', 'exited')]

# TODO: Change the local and test database to postgres


class Park(models.Model):
    name = models.CharField(max_length=100, unique=True)
    maximum_no_cars = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    charge_per_min = models.IntegerField(default=0, null=False, blank=False)
    first_thirty_free = models.BooleanField(default=False, null=False, blank=False)

    def number_of_parked_cars(self):
        return self.parkingtickets.filter(status=STATUS[0][1]).count()

    def has_space(self):
        """Check if currently parked cars are not more than
        maximum_no_cars
        """
        parked_cars = self.parkingtickets.filter(status=STATUS[0][1])
        return parked_cars.count() < (self.maximum_no_cars)

    def get_days_specific_parkingtickets(self, days=None):
        if not days:
            return self.parkingtickets.all()
        parked_time = timezone.now() - timedelta(days=int(days))
        return self.parkingtickets.filter(entry_time__lte=parked_time)

    def is_parked(self, plate_number):
        parked = self.parkingtickets.filter(
            plate_number=plate_number, status=STATUS[0][1])
        return parked.exists()

    def get_amount_paid(self, days=None):
        # TODO: Use object attr to abstract this function to a util file
        def sum_fee_paid(x, y):
            a = x.fee_paid if issubclass(type(x), models.Model) else x
            b = y.fee_paid if issubclass(type(y), models.Model) else y
            return a + b
        parkingtickets = self.get_days_specific_parkingtickets(days)
        return functools.reduce(sum_fee_paid, parkingtickets, 0.0)

    def get_amount_owned(self, days=None):
        def sum_amount_owned(x, y):
            a = x.amount_owed() if issubclass(type(x), models.Model) else x
            b = y.amount_owed() if issubclass(type(y), models.Model) else y
            return a + b
        parkingtickets = self.get_days_specific_parkingtickets(days)
        return functools.reduce(sum_amount_owned, parkingtickets, 0.0)

    def __str__(self):
        return self.name


class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # TODO: Rename to park
    parks = models.ForeignKey(Park, related_name="tenants",
                              on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


class TenantCars(models.Model):
    plate_number = models.CharField(max_length=9, validators=[plate_number_validator])
    tenant = models.ForeignKey(Tenant, related_name='cars', on_delete=models.CASCADE)
    # TODO: Add serializer and viewset for TenantCars


class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=9,
                                    validators=[plate_number_validator])
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    fee_paid = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS, default="parked", max_length=7)
    date_modified = models.DateTimeField(auto_now=True)
    park = models.ForeignKey(
        Park, related_name="parkingtickets", on_delete=models.CASCADE)
    tenant = models.ForeignKey(
        Tenant, related_name='tenant_parkingtickets', on_delete=models.CASCADE,
        blank=True, null=True)

    def get_ticket_fee(self):
        # TODO: Use park parking rate to calculate fee
        THIRTY_MIN = 1800
        ONE_HOUR = 3600
        TWO_HOURS = 7200

        stayed_time = timezone.now() - self.entry_time
        stayed_time_seconds = stayed_time.total_seconds()

        if stayed_time_seconds <= THIRTY_MIN:
            return 0.0
        elif stayed_time_seconds <= TWO_HOURS:
            return math.ceil(stayed_time_seconds/ONE_HOUR) * 200
        else:
            return 400.0 + math.ceil((stayed_time_seconds - TWO_HOURS) / ONE_HOUR) * 100

    def checkout(self):
        if not self.checkout_time:
            self.checkout_time = timezone.now()
        return self.get_ticket_fee()

    def amount_owed(self):
        if self.tenant:
            return 0.0
        return self.get_ticket_fee() - self.fee_paid

    def exit_park(self):
        can_exit = self.amount_owed() <= 0
        if can_exit:
            self.status = 'exited'
            self.exit_time = timezone.now()
            self.save()
        return can_exit

    def pay_ticket(self, amount):
        self.fee_paid += amount
        self.save()

    class Meta:
        indexes = [
            models.Index(fields=['plate_number']),
            models.Index(fields=['park']),
            models.Index(fields=['plate_number', 'park']),
        ]
