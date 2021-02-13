from django.conf.urls import url,include
from Members import views
from .views import *
from .functions import verify_otp, generate_otp,forgot_password,reset_password
from django.urls import path
from django.views.static import serve
from Gfundsbackend2 import settings

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^links/$', views.LinksPageView.as_view()),
    path('register/', views.MemberRegistration.as_view()),
    path('generate_otp/', generate_otp),
    path('verify/', views.VerifyUser.as_view()),
    path('generateotp/', getOtp),
    path('verifyotp/', verify_otp),
    path('logindata/', views.Login.as_view(), name="login"),
    path('finalregister/', views.MemberFinalRegistration.as_view()),
    path('upcomingfunds/', views.UpcomingFunds.as_view()),
    path('memberdocs/', views.MemberUpload.as_view()),
    path('requesttoforeman/',views.RequestToForeman.as_view()),
    path('requestedfund/',views.MemberRequestedFunds.as_view()),
    path('forgotpassword/',forgot_password),
    path('resetpassword/',reset_password),
    path ('viewmemberprofile/',views.ViewMemberProfile.as_view()),
    path('editmemberprofile/',views.EditMemberProfile.as_view()),
    path('runningmemberlist/',views.Running_Member_List.as_view()),
    path('viewdashboard/',views.View_dashboard.as_view()),
    path('trans/',views.MemberTransaction.as_view()),
    path('auctiontransid/',views.AuctionTransactions.as_view()),
    path('runningdetail/',views.FundRunningDetails.as_view()),
    path('timeaction/',views.AuctionTime.as_view()),
    path('checkfinalaction/',views.Check_Repeated_Auction.as_view()),
    path('transactiondata/',views.TransactionRecord.as_view()),
    path('auctionhistory/',views.MemberAuctionalloted.as_view()),
    path('closedchits/',views.Closedfunds.as_view()),
    path('memberhome/',views.MemberHomegraph.as_view()),
    path('fundHistory/', views.GetFundDetails.as_view()),
    path('picupdate/', views.ProfilePicUpdate.as_view()),
    path('getClosedGrap/',views.GetClosedFunds.as_view()),
    path('profiledp/',views.ProfilePic.as_view()),
    path('uploadcibilfile/',views.Uploadcibilfile.as_view()),
    path('getcibilfile/',views.GetCibiFfile.as_view()),
    path('Profiledata/',views.Profiledata.as_view()),
    path('getmemdocs/', views.Getmembdoc.as_view()),
    path('uploadpics/', views.Memberdocsupload.as_view()),
    path('getParticularTransaction/',views.GetTransData.as_view()),
    path('mesfornewmem/', views.HelpMesForNewMem.as_view()),
    path('statusForMemGraph/', views.StatusForMemGraph.as_view()),


]
