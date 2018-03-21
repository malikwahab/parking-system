from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from ticketingapp.models import ParkingTicket, Mall


class TestParkingTicket(TestCase):

    def setUp(self):
        mall = Mall.objects.create(name='ICM')
        self.parkingticket = ParkingTicket.objects.create(
            plate_number="ABC-123ED",
            mall=mall
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
