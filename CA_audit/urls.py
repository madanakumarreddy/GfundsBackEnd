from django.conf.urls import url
from django.urls import path

from Gfundsbackend2 import settings
from CA_audit import views
urlpatterns=[
  path("caregistration/",views.CaRegistation.as_view()),
  path("ca_groups/", views.CA_Groups.as_view()),
  path("get_auctioncount/", views.GetAuctionCount.as_view()),


]