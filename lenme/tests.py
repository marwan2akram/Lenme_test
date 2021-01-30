import json
from .models import *
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .serializers import *


class LoanRequestsCreateAPIViewTestCase(APITestCase):
    create_loan_url = reverse("lenme:create-loan")
    create_offer_url = reverse("lenme:create-offer")

    def setUp(self):
        self.investor = Investor.objects.create(name="Akram", email="akram@snow.com", balance=50000)
        self.borrower = Borrower.objects.create(name="Marwan", email="Marwan@snow.com")
        # In case we have user authentication
        # self.token = Token.objects.create(user=self.user)
        # self.api_authentication()

    # Test loan requests can be created
    def test_create_loan(self):
        number_of_loans_before = Loan.objects.count()
        response = self.client.post(
            self.create_loan_url,
            {"Borrower": self.borrower.id, "amount": 5000, "period": 6}
        )
        self.assertEqual(201, response.status_code)
        self.assertGreater(Loan.objects.count(), number_of_loans_before)

    # Test if the investor balance is not sufficient for the funding
    def test_investor_balance(self):
        loan = Loan.objects.create(Borrower=self.borrower, amount=50001, period=6)
        response = self.client.post(
            self.create_offer_url,
            {"investor": self.investor.id, "loan": loan.id, "interest": 15}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.data['detail'], "insufficient funds")

    # Test if the loan status was changed after successful funding
    def test_loan_status(self):
        loan = Loan.objects.create(Borrower=self.borrower, amount=4999, period=6)
        offer = Offer.objects.create(investor=self.investor, loan=loan)
        offer_status_before = offer.accepted

        accept_offer_url = reverse("lenme:accept-offer", kwargs={'pk': offer.id})
        response = self.client.post(
            accept_offer_url,
        )

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(Offer.objects.get(id=offer.id).accepted, offer_status_before)
        self.assertEqual(Loan.objects.get(id=loan.id).status, "Funded")

