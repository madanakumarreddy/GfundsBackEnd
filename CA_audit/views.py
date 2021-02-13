from django.shortcuts import render

from Foreman.models import ForemanProfile, Chits,FinalAuctions
from Members.models import Request
from .models import *
from rest_framework.views import APIView
from Members.functions import authUserId, encrypt_password
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from Members.functions import authentication




# Create your views here.
class CaRegistation(APIView):
    def post(self,request):
        print("cadataaaaaaaaaaaa",request.data)
        fullname = request.data['fullname']
        mobile= request.data['username']
        password = request.data['password']
        # dob = request.data['']
        try:
            user=User.objects.get(username=mobile,is_active=True);
            if user:
                return Response("user alredy exit")
        except User.DoesNotExist:
            try:
                with transaction.atomic():
                     user = User()
                     user.first_name = fullname
                     user.username = mobile
                     user.password =  encrypt_password(password)
                     user.is_active = True
                     user.id=authUserId()
                     user.save();
                     userid = User.objects.get(id=user.id)
                     print("hjdssssssssssssssssssss",userid)
                     profile= CaProfile()
                     profile.user=userid
                     profile.first_name=fullname
                     profile.mobile_number=mobile
                     profile.password= encrypt_password(password)
                     profile.save()
                     return Response("Registration success", status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response("Registration failed", status=status.HTTP_400_BAD_REQUEST)


class CA_Groups(APIView):
    def get(self,request):
        print(request.data)
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            user1 = CaProfile.objects.get(user=user)
            if user1:
                data1 = Chits.objects.filter()
                data = data1.values()
                print("dataaaaaaaaaaaaaaaaaaaaa",data)
                for idval, pic in enumerate(data):
                    data[idval]['company_logo'] = data1[idval].company_logo.url
                return Response(data)




        except Exception as e:
            print(e)
            return Response("ERROR",status=status.HTTP_400_BAD_REQUEST)



class GetAuctionCount(APIView):
    def post(self,request):
        print("dddddddd", request.data);
        data = FinalAuctions.objects.filter(chit = request.data['chit'], foreman = request.data['foreman_id'] ).values().exclude(member=None)
        print("bbbbbbbbbbbb", len(data));
        data1 = FinalAuctions.objects.filter(chit = request.data['chit']).values_list('auction_count', flat=True).exclude(member=None);
        return  Response({'data':data.order_by('id'),'length': data1.order_by('id')})
