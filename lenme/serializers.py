from rest_framework import serializers
from .models import Investor, Borrower,Loan, Offer


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'name', 'balance', 'email']


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'Borrower', 'amount', 'period', 'status', 'paid_payments', 'created_at', 'updated_at']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'investor', 'loan', 'interest', 'accepted', 'created_at']