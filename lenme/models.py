from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

LOAN_CHOICES = (
    ("Not funded", "Not funded"),
    ("Funded", "Funded"),
    ("Completed", "Completed"),
)


class Investor(models.Model):
    name = models.CharField(max_length=50)
    balance = models.FloatField(validators=[MinValueValidator(1)])
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Borrower(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    Borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    period = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=LOAN_CHOICES, default="Not funded")
    paid_payments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.pk


class Offer(models.Model):
    investor = models.ForeignKey(Investor,on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='offers')
    interest = models.PositiveIntegerField(default=15, validators=[MinValueValidator(1), MaxValueValidator(100)])
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.pk