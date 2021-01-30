from django.urls import path
from rest_framework.urls import app_name

from . import views

app_name = "lenme"

urlpatterns = [
    path('', views.index, name='index'),
    path('list-investors', views.get_investors, name='list-investors'),
    path('list-investors/<int:pk>', views.get_investor, name='get-investor'),
    path('list-investors/<int:pk>/offers', views.get_investor_offers, name='list-investors-offers'),
    path('list-borrowers', views.get_borrowers, name='list-borrowers'),
    path('list-borrowers/<int:pk>', views.get_borrower, name='get-borrower'),
    path('list-borrowers/<int:pk>/loans', views.get_borrower_loans, name='get-borrower-loans'),
    path('list-loans', views.get_loans, name='list-loans'),
    path('list-loans/<int:pk>', views.get_loan, name='get-loans'),
    path('list-loans/<int:pk>/offers', views.get_loan_offers, name='get-loan-offers'),
    path('create-investor', views.create_investor, name='create-investor'),
    path('create-borrower', views.create_borrower, name='create-borrower'),
    path('create-loan', views.create_loan, name='create-loan'),
    path('create-offer', views.create_offer, name='create-offer'),
    path('accept-offer/<int:pk>/', views.accept_offer, name='accept-offer'),
    path('make-single-payment/<int:pk>/', views.make_single_payment, name='Make-single-payment'),
    ]
