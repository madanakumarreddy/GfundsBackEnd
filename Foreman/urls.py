from django.conf.urls import url
from Foreman import views
from django.urls import path

urlpatterns = [
    path('foremanregister/',views.ForemanRegistration.as_view()),
    path('newchit/',views.NewChit.as_view()),
    path('fileadressupload/',views.ForemanUpload.as_view()),
    path('foremanfinalregister/', views.ForemanFinalRegister.as_view()),
    path('foremanview/',views.ForemanViewProfile.as_view()),
    path('editforeman/',views.EditForemanProfile.as_view()),
    path('foremanrequestedchits/', views.Foreman_Requested_Chits.as_view()),
    path('foremanrequest/', views.Forman_Reuqest.as_view()),
    path('membersadd/', views.Members_Add.as_view()),
    path('addedmembers/', views.Added_members.as_view()),
    path('approvetrans/', views.Approve_trans.as_view()),
    path('auctiondate/',views.AuctionDate.as_view()),
    path('foremanhome/',views.ForemanHome.as_view()),
    path('foremanrunning/',views.ForemanRunningFunds.as_view()),
    path('membertransid/',views.MemberAuctiontrans.as_view()),
    path('auctiontransactionhistory/',views.TransactionAuctionHistory.as_view()),
    path('savebid/',views.Auctiondata.as_view()),
    path('getlist/',views.GetAuctionList.as_view()),
    path('runningtransapprove/',views.Approve_auction_call_transaction.as_view()),
    path('graphdetails/',views.Graph_details.as_view()),
    path('govtcopy/',views.FdUpload.as_view()),
    path('Member_Chit_Details/',views.MemberFundDetails.as_view()),
    path('memdetails/',views.ViewMemberProfile.as_view()),
    path('foremanpic/', views.ForemanPicUpdated.as_view()),
    path('getForemanPic/',views.GetForemanPic.as_view()),
    path('saveTransaction/',views.SaveTransaction.as_view()),
    path('getupload/',views.Getupload.as_view()),
    path('foremanclosedchits/',views.ForemanClosedChits.as_view()),
    path('auctionupdate/',views.auctionupdate.as_view()),
    path('updateForemanScore/', views.UpdateForemanScore.as_view()),



]