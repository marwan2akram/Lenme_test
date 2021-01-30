from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InvestorSerializer, BorrowerSerializer, LoanSerializer, OfferSerializer
from .models import Investor, Borrower, Loan, Offer
from django.core import serializers
from rest_framework import status


def index(request):
    return HttpResponse(" You're at the lenme index. ")


# Create an endpoint to handle GET requests
#   for all available investors.


@api_view(['GET'])
def get_investors(request):
    investors = Investor.objects.all()
    serializer = InvestorSerializer(investors, many=True)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
# to get investor based on pk

@api_view(['GET'])
def get_investor(request, pk):
    investor = get_object_or_404(Investor, id=pk)
    serializer = InvestorSerializer(investor, many=False)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
#   for all available investor offers.


@api_view(['GET'])
def get_investor_offers(request, pk):
    investor = get_object_or_404(Investor, id=pk)
    investor_offers = investor.offer_set.all()
    serializer = OfferSerializer(investor_offers, many=True)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
#   for all available borrowers.


@api_view(['GET'])
def get_borrowers(request):
    borrowers = Borrower.objects.all()
    serializer = BorrowerSerializer(borrowers, many=True)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
# to get borrower based on pk


@api_view(['GET'])
def get_borrower(request, pk):
    borrower = get_object_or_404(Borrower, id=pk)
    serializer = BorrowerSerializer(borrower, many=False)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
#   for all available borrower loans.


@api_view(['GET'])
def get_borrower_loans(request, pk):
    borrower = get_object_or_404(Borrower, id=pk)
    borrower_loans = borrower.loan_set
    serializer = LoanSerializer(borrower_loans, many=True)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
#   for all available loans.


@api_view(['GET'])
def get_loans(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
# to get loan based on pk


@api_view(['GET'])
def get_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    serializer = LoanSerializer(loan, many=False)
    return Response(serializer.data)


# Create an endpoint to handle GET requests
#   for all available loan offers.


@api_view(['GET'])
def get_loan_offers(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    offers= loan.offers.all()
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


# Create an endpoint to POST a new investor.
# which will require the name, balance, and email.

@api_view(['POST'])
def create_investor(request):
    serializer = InvestorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create an endpoint to POST a new borrower.
# which will require the name, and email.

@api_view(['POST'])
def create_borrower(request):
    serializer = BorrowerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create an endpoint to POST a new loan,
# which will require the Borrower, amount, and period.


@api_view(['POST'])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create an endpoint to POST a new offer,
# which will require the Borrower, amount, and period.
# the offer will not created if the investor don't have Sufficient fund.

@api_view(['POST'])
def create_offer(request):
    serializer = OfferSerializer(data=request.data)
    if serializer.is_valid():
        investor_id = request.data["investor"]
        investor = get_object_or_404(Investor, id=investor_id)
        loan_id = request.data["loan"]
        loan = get_object_or_404(Loan, id=loan_id)
        # Assume the lanme fee for the transaction = 3.0 $
        lenme_fee = 3
        if investor.balance > (loan.amount + lenme_fee):
            if loan.status == "Not funded":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "This loan is already funded"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create an endpoint to accept  an offer,
# the offer accepted field changes to True,
# the lone status changes to funded,
# The loan amount + lenme fee are deducted from the investor's balance.


@api_view(['POST'])
def accept_offer(request, pk):
    offer = get_object_or_404(Offer, id=pk)
    if not offer.accepted:
        offer.accepted = True
        offer.save()
        loan = offer.loan
        loan.status = "Funded"
        loan.save()
        # Assume the lanme fee for the transaction = 3.0 $
        lenme_fee = 3
        investor = offer.investor
        investor.balance -= (loan.amount + lenme_fee)
        investor.save()
        serializer = LoanSerializer(loan, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # you accepted the offer Your loan has been funded
    return Response({"detail": "you already accepted this offer"}, status=status.HTTP_400_BAD_REQUEST)


# Create an endpoint to make a single payment of an loan,
# Once all the payments are successfully paid back to the investor,
# the loan status will be changed to `Completed`.


@api_view(['POST'])
def make_single_payment(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    if loan.status == "Funded":
        if loan.paid_payments == loan.period:
            loan.status = "Completed"
            loan.save()
            serializer = LoanSerializer(loan, many=False)
            return Response({"detail": "this loan is completed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            loan.paid_payments += 1
            loan.save()
            offer = loan.offers.first()
            investor = offer.investor
            single_payment = (loan.amount + (loan.amount*((offer.interest/1200)*loan.period)))/loan.period
            investor.balance += round(single_payment, 2)
            investor.save()
            serializer = LoanSerializer(loan, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif loan.status == "Not funded":
        return Response({"detail": "this loan is not funded"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "this loan is completed"}, status=status.HTTP_400_BAD_REQUEST)
