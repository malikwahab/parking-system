from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

plate_number_validator = RegexValidator("([A-Za-z]{3}\-\d{3}[A-Za-z]{2})", "Plate Number are in the format ABC-123DE")
STATUS = [('0', 'parked'), ('1', 'exited')]


class Mall(models.Model):
    name = models.CharField(max_length=100)
    maximum_no_cars = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=9,
                                    validators=[plate_number_validator])
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True)
    fee_paid = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS, default="parked", max_length=7)
    date_modified = models.DateTimeField(auto_now=True)
    mall = models.ForeignKey(Mall, related_name="mall", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['plate_number']),
            models.Index(fields=['mall']),
            models.Index(fields=['plate_number', 'mall']),
        ]
