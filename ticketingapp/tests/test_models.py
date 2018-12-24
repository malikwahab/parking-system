from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from ticketingapp.models import ParkingTicket, Park

# TODO: Fix the test and write new test

class TestParkingTicket(TestCase):

    def setUp(self):
        park = Park.objects.create(name='ICM')
        self.parkingticket = ParkingTicket.objects.create(
            plate_number="ABC-123ED",
            park=park
        )

    def test_first_thirty_minutes(self):

        start_time = datetime.now()

        self.parkingticket.entry_time = \
            timezone.make_aware(start_time - timedelta(minutes=25))

        self.parkingticket.checkout_time = timezone.make_aware(start_time)

        # assert ticket_fee is zero
        self.assertEqual(self.parkingticket.get_ticket_fee(), 0)

        # assert can exit
        self.assertTrue(self.parkingticket.exit_park())

    def test_first_one_hour(self):

        start_time = datetime.now()

        self.parkingticket.entry_time = \
            timezone.make_aware(start_time - timedelta(minutes=50))

        self.parkingticket.checkout_time = timezone.make_aware(start_time)

        # assert ticket_fee
        self.assertEqual(self.parkingticket.get_ticket_fee(), 200)

    def test_one_two_hours(self):

        start_time = datetime.now()

        self.parkingticket.entry_time = \
            timezone.make_aware(start_time - timedelta(hours=1, minutes=50))

        self.parkingticket.checkout_time = timezone.make_aware(start_time)

        # assert ticket_fee
        self.assertEqual(self.parkingticket.get_ticket_fee(), 400)

    def test_above_two_hours(self):

        start_time = datetime.now()

        self.parkingticket.entry_time = \
            timezone.make_aware(start_time - timedelta(hours=2, minutes=50))

        self.parkingticket.checkout_time = timezone.make_aware(start_time)

        # assert ticket_fee
        self.assertEqual(self.parkingticket.get_ticket_fee(), 500)

        self.parkingticket.entry_time = \
            timezone.make_aware(start_time - timedelta(hours=5, minutes=50))

        self.assertEqual(self.parkingticket.get_ticket_fee(), 800)

    def test_fee_paid(self):

        self.parkingticket.entry_time = \
            timezone.make_aware(datetime.now() - timedelta(hours=2, minutes=50))

        ticket_fee = self.parkingticket.checkout()

        self.parkingticket.pay_ticket(ticket_fee)

        # assert Fee paid
        self.assertEqual(self.parkingticket.fee_paid, ticket_fee)

        # assert can exit
        self.assertTrue(self.parkingticket.exit_park())

    def test_partial_payement(self):

        self.parkingticket.entry_time = \
            timezone.make_aware(datetime.now() - timedelta(hours=2, minutes=50))

        ticket_fee = self.parkingticket.checkout()

        self.parkingticket.pay_ticket(ticket_fee - 300)

        # assert can't exit until fully paid
        self.assertFalse(self.parkingticket.exit_park())

        self.parkingticket.pay_ticket(300)

        # assert fee completed
        self.assertEqual(self.parkingticket.fee_paid, ticket_fee)

        # assert can exit store
        self.assertTrue(self.parkingticket.exit_park())


class TestMall(TestCase):

    def setUp(self):
        self.park = Park.objects.create(
            name='ICM', maximum_no_cars=2)
        self.parkingticket = ParkingTicket.objects.create(
            plate_number="ABC-123ED",
            park=self.park
        )

    def test_has_space(self):
        # assert has space
        self.assertTrue(self.park.has_space())
        
        ParkingTicket.objects.create(
            plate_number="ZYX-984SD",
            park=self.park
        )

        # assert no space
        self.assertFalse(self.park.has_space())

    def test_is_parked(self):
        # assert car is parked
        self.assertTrue(self.park.is_parked('ABC-123ED'))

        # assert car is not parked
        self.assertFalse(self.park.is_parked('ZXC-456LK'))
    
    def test_amount_paid(self):
        self.parkingticket.pay_ticket(300)

        # assert amount paid
        self.assertEqual(self.park.get_amount_paid(), 300)
