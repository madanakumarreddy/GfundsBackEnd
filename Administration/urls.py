from django.urls import path
from django.views.static import serve

from Administration import views
from django.conf.urls import url
from django.urls import path

from Gfundsbackend2 import settings

urlpatterns = [
    path('adminmanagefunds/',views.manage_funds.as_view()),
    path ('updatemanagefunds/',views.UpdateManageFunds.as_view()),
    path('manageforeman/', views.ManageForemanFunds.as_view()),
    path('updateforeman/',views.UpdateManageForeman.as_view()),
    path('approveforeman/',views.ApproveForeman.as_view()),
    path('managechits/', views.AdminUpcomingFunds.as_view()),
    path('approveupcomingchit/', views.ApproveUcomingFunds.as_view()),
    path('memberlist1/', views.memberlist1.as_view()),
    path('approvemember/', views.Approvemember.as_view()),
    path('memberdata1/',views.Memberdetail.as_view()),
    path('editapprovemem/', views.EditApproveMem.as_view()),
    path('homeupcomingfunds/',views.HomeUpcomingfunds.as_view()),
    path('homerunningfunds/',views.HomeRunningfunds.as_view()),
    path('filter/', views.Chit_Details.as_view()),
    path('adminrun/',views.AdminRunChits.as_view()),
    path('getExecutiveinfo/', views.GetExecutiveinfo.as_view()),

]