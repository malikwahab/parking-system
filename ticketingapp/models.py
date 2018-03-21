import math

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

plate_number_validator = RegexValidator("([A-Za-z]{3}\-\d{3}[A-Za-z]{2})", "Plate Number are in the format ABC-123DE")
STATUS = [('0', 'parked'), ('1', 'exited')]


class Mall(models.Model):
    name = models.CharField(max_length=100)
    maximum_no_cars = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=9,
                                    validators=[plate_number_validator])
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    fee_paid = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS, default="parked", max_length=7)
    date_modified = models.DateTimeField(auto_now=True)
    mall = models.ForeignKey(Mall, related_name="mall", on_delete=models.CASCADE)

    def get_ticket_fee(self):
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
            models.Index(fields=['mall']),
            models.Index(fields=['plate_number', 'mall']),
        ]
