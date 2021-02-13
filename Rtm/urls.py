from django.urls import path
from Rtm import views
urlpatterns=[
    path('Newloan/',views.RaiseLoan.as_view()),
    path('loan_request/',views.Request_loan.as_view()),
    path('approve_request/',views.Approve_req.as_view()),
    path('getsilverloantype/',views.Getsilverloan.as_view()),
    path('getpaltinumloantype/',views.Getplatinumloan.as_view()),
    path('getgoldloantype/',views.Getgoldloan.as_view()),
]