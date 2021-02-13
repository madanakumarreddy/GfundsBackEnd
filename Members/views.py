# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from operator import itemgetter
from builtins import Exception

from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from django.contrib.auth.models import User
from rest_framework import status
from django.db import transaction
import logging
import traceback
from rest_framework.views import APIView
# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import datetime

from CA_audit.models import CaProfile
from Rtm.models import MemberLoanDetails, Loan
from .functions import authentication,generate_otp,encrypt_password,get_features,authUserId
import json
import jwt
from Foreman.models import ForemanProfile, Chits, RunningChits,FinalAuctions, Auctions
from Administration.models import ExecutiveProfile, Resellers_Referel
from .serializers import MemberUpdateSerializer, MemberEditSerializer,MemberDashboardViewSerializer, \
    FinalAuctionsViewSerializer
from .models import Request,Transactions
from django.db.models import Q
from dateutil.relativedelta import relativedelta




from Members.models import MemberProfile

logger = logging.getLogger(__name__)


def get_member_id():
    count = MemberProfile.objects.all().count()
    print ("MYYYYYYY COUNTTTTTTTTTTTTTTTTTTTT",count)
    if count != 0:
        print ("inside ifffffffffff")
        customid = "M" + str(count + 1)
        print ("R$$$$$$$$$$$$$$$$$$",customid)
    else:
        customid = "M1"
    return customid

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class LinksPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'links.html', context=None)

class MemberRegistration(APIView):
    def post(self,request):
        full_name = request.data['first_name']
        dateofbirth = request.data['date_of_birth'][4:24]
        print("front date",dateofbirth,type(dateofbirth))
        date_of_birth=datetime.datetime.strptime(dateofbirth, "%b %d %Y %H:%M:%S").date()
        print("sacccccc",date_of_birth,type(date_of_birth))
        finaldate = datetime.datetime.strftime(date_of_birth,'%Y-%m-%d')
        # date_of_birth = dateofbirth
        print("DAAAAAAAAAAAA",finaldate)
        mobile_number = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=mobile_number, is_active=True)
            if user:
                return Response("User already exists", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            try:
                print("i m inside!!!!!!!!!!!!!!!!!!!!!!!!!!")
                with transaction.atomic():

                    user = User()
                    print("witttttttthhhhhhhhhhhhhhhhhhhhhhh")
                    encrypt = encrypt_password(password)
                    # user.id = self.auth_get_id()
                    user.username = mobile_number
                    user.password = encrypt
                    user.last_name = ""
                    user.first_name = full_name
                    user.is_active = True
                    user.id = authUserId()
                    user.save()
                    print ("AFTERRRRRRRRRR USER SAVEEEEEEEEEEEEEEEEEEEEE")
                    userid = User.objects.get(id=user.id)
                    print("idddddddddddd frommmmmmm userrrrrrr",userid)
                    profile = MemberProfile()
                    profile.user = userid
                    profile.full_name = full_name
                    profile.date_of_birth = finaldate
                    profile.mobile_number = mobile_number
                    profile.id = get_member_id()
                    print ("@@@@@@@@@@@@@2",profile.id)
                    profile.save()
                    print("Afterrrrrrrrrrrrrrrrrr saveeeeeeeeeee in proooooooooo")
                    # time = datetime.datetime.now()
                    # logger.info("######################################################")
                    # logger.info("New Member" + full_name + " registered  " + "(" + str(mobile_number) + ")" + " " +
                    #             profile.id +
                    #             " @ " + str(time))
                    # logger.info(str(profile.id) + " Registered @" + str(time))
                    # logger.info("######################################################")
                return Response("Registration success", status=status.HTTP_200_OK)
            except Exception as e:
                # tb = traceback.format_exc()
                print(e)
                # logger.info("######################################################")
                # logger.info("Profile Update " + str(id) + " " + " Failed")
                # logger.info("######################################################")
                return Response("Registration failed", status=status.HTTP_400_BAD_REQUEST)
    # def auth_get_id(self):
    #     count = User.objects.all().count()
    #     return count+1

# class VerifyUser(APIView):
#     def post(self,request):
#         try:
#             token = request.META['HTTP_AUTHORIZATION']
#             print("tttttttttt",token)
#             data = {'token': token}
#             valid_data = VerifyJSONWebTokenSerializer().validate(data)
#             user = valid_data['user']
#             data = User.objects.filter(id=user.id).values()
#             print("rrrrrrrrrrrr",data)
#             return Response(data)
#         except Exception as e:
#             print("hi",e)
#             return Response("ttttttttttt")


class VerifyUser(APIView):
    def post(self,request):
        user = authentication(request.META['HTTP_AUTHORIZATION'])
        data = User.objects.filter(id=user).values()
        return Response(data)

@api_view(['POST'])
def getOtp(request):
    otp =  generate_otp(request)
    return Response(otp)


# class Login(APIView):
#     def post(self, request):
#         if not request.data:
#             return Response("Please provide username/password")
#
#         username = request.data['username']
#         password = request.data['password']
#         encrypt = encrypt_password(password)
#         name = User.objects.filter(username=username)
#         if not name:
#             return Response("Invalid username")
#         else:
#             try:
#                 user = User.objects.get(username=username,password=encrypt)
#                 print("userrrrrrrrrrrrrrrrr",user)
#                 if user:
#                     print("insideeeeeeeee IFFFFFFFFFFfffffff")
#                     if user.is_active:
#                         if str(user.password) == encrypt:
#                             profile = MemberProfile.objects.filter(user=user.id)
#                             print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPP",profile)
#                             if profile:
#                                 if profile[0].front_photo:
#                                     profilepic = profile[0].front_photo.url
#                                 else:
#                                     profilepic = ''
#                                 print("profpicccccccccccccccccccccc",profilepic)
#                             if not profile:
#                                 print("Foremannnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
#                                 profile = ForemanProfile.objects.filter(user=user.id)
#                                 print("Fore@@@@@@@@@@@@@@@@@@@@@@@@@sssss", profile)
#                                 if profile:
#                                     if profile[0].front_photo:
#                                         profilepic = profile[0].front_photo.url
#                                     else:
#                                         profilepic = ''
#                                     print("FORRRRRRRRRRRRRRRRRRRRRKLLLLLLLLLLLLLLLLLLLLL",profilepic)
#                                 if not profile:
#                                     profile = ExecutiveProfile.objects.filter(user=user.id)
#                                     print("888888888888888888",profile)
#                                     profilepic = ''
#
#                                     feature = get_features(profile[0].role, profile[0])
#                             time = datetime.datetime.now()
#                     payload = {
#                         'id': user.id,
#                         'exp': datetime.datetime.now() + relativedelta(hours=1)
#                     }
#                     jwt_token = jwt.encode(payload, "SECRET_KEY")
#
#                     MemberProfile.objects.filter()
#                     data = {'token': jwt_token,'role': profile.values()}
#                     return Response(data)
#             except Exception as e:
#                 print("exxxxxxxxx",e)
#                 return Response("invalid password")


class Login(APIView):
    def post(self, request):
        if not request.data:
            return Response("Please provide username/password")

        username = request.data['username']
        password = request.data['password']
        encrypt = encrypt_password(password)
        name = User.objects.filter(username=username)
        if not name:
            return Response("Invalid username")
        else:
            try:
                user = User.objects.get(username=username,password=encrypt)
                if user:
                    if user.is_active:
                        if str(user.password) == encrypt:
                            profile = MemberProfile.objects.filter(user=user.id).values()
                            if not profile:
                                profile = ForemanProfile.objects.filter(user=user.id).values()
                                print("sssss", profile)
                                if not profile:
                                    profile = CaProfile.objects.filter(user=user.id).values()
                                    print("caaaaaaaaaaa",profile)
                                    if not profile:
                                        profile = ExecutiveProfile.objects.filter(user=user.id).values()
                                        feature = get_features(profile[0]['role'], profile[0])
                            time = datetime.datetime.now()
                    payload = {
                        'id': user.id,
                        'exp': datetime.datetime.now() + relativedelta(hours=1)
                    }
                    jwt_token = jwt.encode(payload, "SECRET_KEY")
                    # token = json.dumps(str(jwt_token))
                    # print("toooooooooooooo",token)
                    data = {'token': jwt_token,'role': profile[0]}
                    return Response(data)
            except Exception as e:
                print("exxxxxxxxx",e)
                return Response("invalid password")



class MemberFinalRegistration(APIView):
    def post(self, request):
        try:
            print("9999999999999999999999999",request.data['user'])
            print("yyyyyyyyyyyyyyyyyyyyyy",type(request.data['user']))
            print("aaaaaaaabbbbbbbbbbbbbcccccccc",request.data)

            user = authentication(request.META['HTTP_AUTHORIZATION'])
            print("userrrrrr",user)
            data = MemberProfile.objects.get(user=user)
            print("66666666666",data)
            x = json.loads(request.data['user'])
            if x['marital_status'] != 'Unmarried' and x['marital_status'] !='Spouse Deceased' and x['marital_status'] !='Divorcee':
                print("unnnnnnnnnnnnnnn")
                a=x['dat_of_marriage']
                c=datetime.datetime(int(a[0:4]),int(a[5:7]),int(a[8:10])).date()
                x['dat_of_marriage'] =c
            # print("000000000000000000000",type(x['a']),type(x['ifsc_code']),type(x))
            # x['ifsc_code'] = str(x['a'])+ str(x['ifsc_code'])
            serial = MemberUpdateSerializer(data,x)
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            if serial.is_valid(raise_exception=True):
                serial.save()
                print("afterrrrrrrrrrrrrrrrrrrr")
                if request.data['profile']:
                    data.front_photo = request.data['profile']
                    data.save()
                    print("hiii")
                    return Response("success",status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UpcomingFunds(APIView):
    def get(self,request):
        print("requesteeeeeeeeeeeeee",request.data)
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        profile = MemberProfile.objects.filter(user=userid)
        request = set(Request.objects.filter(member_id=profile[0].id).values_list('chit_id', flat=True))
        funds=Chits.objects.filter(status = 'UPCOMING',check=True).exclude(id__in=request).order_by('-id')
        print ("upcoming",funds)
        funds_dict = funds.values()
        chits = Chits.objects.filter(id__in=request, check=True, status="UPCOMING")
        # requestcount = Request.objects.filter(member_id=profile[0].id).values('chit_id').distinct().count()
        requestcount=chits.values().count()
        for i,fund in enumerate(funds_dict):
            if fund['company_logo'] == '':
                fund['company_logo'] = ''
            else:
                fund['company_logo'] = funds[i].company_logo.url

            print("8888888",i,fund)
        chitcount = Chits.objects.filter(status='UPCOMING',check=True).exclude(id__in=request)
        count = chitcount.count()
        data = {"upcomingfunds":funds_dict,"count":count,"requestcount":requestcount}
        return Response(data)

class MemberUpload(APIView):
    def post(self,request):
        print("$$$$$$$$$$$$$$$$$$", request.data,len(request.data));
        try:
            userid= authentication(request.META['HTTP_AUTHORIZATION'])
            member = MemberProfile.objects.get(user=userid)
            if member:
                if 'PresentAddressProof' in request.data:
                    member.present_address_proof = request.data['PresentAddressProof']
                if 'BankStatement' in request.data:
                    member.bank_statement = request.data['BankStatement']
                if 'Aadharcard' in request.data:
                    member.aadharimage = request.data['Aadharcard']
                if 'PanCard' in request.data:
                    member.panimage = request.data['PanCard']
                if 'PaySlip1' in request.data:
                    member.pay_slip1 = request.data['PaySlip1']
                if 'PaySlip2' in request.data:
                    member.pay_slip2 = request.data['PaySlip2']
                if 'PaySlip3' in request.data:
                    member.pay_slip3 = request.data['PaySlip3']
                if 'EmployeeIDCard' in request.data:
                    member.employe_id_card = request.data['EmployeeIDCard']
                member.save()
                return Response("succsessfully saved")
        except Exception as e:
            print(e)
            return Response(status = status.HTTP_400_BAD_REQUEST)

class RequestToForeman(APIView):
    def post(self,request):
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        member = MemberProfile.objects.filter(user = userid)
        chitid = request.data['id']
        count = request.data['count']
        chit = Chits.objects.filter(id=chitid)
        foreman = ForemanProfile.objects.filter(id=chit[0].foreman_id)
        for i in range(0,len(count)):
            data = Request.objects.filter(member_id=member[0].id,foreman_id=foreman[0].id,chit_id = chitid)
            if not data:
                req = Request()
                req.member_id = member[0].id
                req.member_name = member[0].full_name
                req.member_number = member[0].mobile_number
                req.credit = member[0].credit_limit
                req.foreman_id = foreman[0].id
                req.foreman_name = foreman[0].full_name
                req.foreman_number = foreman[0].mobile_number
                req.company_name = chit[0].company_name
                req.chit_name = chit[0].chit_number
                req.chit_id = chitid
                req.member_chit_count = 1
                req.save()
                if int(member[0].credit_limit) > int(chit[0].chit_amount):
                    req.save()
                    data1 = " Our executive will going to contact you regarding fraternity fund details." \
                            " Thank You."
                else:
                    data1 = "Your Credit Limit is too low to send request for respective fraternity fund company. Please contact our " \
                        "customer service."
            else:
                val = Request.objects.filter(chit_id=chit[0].id, member_id=member[0].id,foreman_id=foreman[0].id).values_list('member_chit_count',
                                                                                                   flat=True).last()
                req = Request()
                req.member_chit_count = int(val) + 1;
                req.member_id = member[0].id
                req.credit = member[0].credit_limit
                req.member_name = member[0].full_name
                req.member_number = member[0].mobile_number
                req.foreman_id = foreman[0].id
                req.company_name = chit[0].company_name
                req.chit_name = chit[0].chit_number
                req.foreman_name = foreman[0].full_name
                req.foreman_number = foreman[0].mobile_number
                req.chit_id = chit[0].id
                req.save()
        return Response("saved successfully")

class MemberRequestedFunds(APIView):
    def get(self,request):
        try:
            userid = authentication(request.META['HTTP_AUTHORIZATION'])
            member = MemberProfile.objects.filter(user=userid)
            request = set(Request.objects.filter(member_id=member[0].id).values_list('chit_id', flat=True))
            chitrequest = Request.objects.filter(member_id=member[0].id).values('chit_id').distinct()
            count =chitrequest.count()
            print("chhhhhhhhhh",count)
            chits = Chits.objects.filter(id__in=request,check=True)
            chit_dict = chits.values()
            for i,chit in enumerate(chit_dict):
                print("oooooooooo",chit)
                if chit['company_logo'] == '':
                    chit['company_logo'] = ''
                else:
                    chit['company_logo'] = chits[i].company_logo.url
                data = Request.objects.filter(chit_id=chits[i],member_id=member[0].id).count()
                print("iiiiiiiiiiiii",data)
                chit['mcount'] = data
                chit['status'] = 'REQUESTED'
            data = {"chit_dict":chit_dict,"count":count}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response("errrorrr")
            print(e)

class ViewMemberProfile(APIView):
    def get(self,request):
        print(request.data)
        try:
            userid = authentication(request.META['HTTP_AUTHORIZATION'])
            member = MemberProfile.objects.get(user = userid)
            print(member)
            if member:
                print("insideeee ifffffffffffff")
                prof = MemberProfile.objects.filter(id=member).values()
                print(prof)
                data = {"data":prof}
            return Response(data)
        except Exception as e:
            print(e)





class EditMemberProfile(APIView):
    def post(self,request):
        print("aaaaaaaaaaaaaa", request.data)
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            member = MemberProfile.objects.get(user=user)
            # if(request.data['marital_status']=='Unmarried'):
            #     request.data['dat_of_marriage']=''

            data = MemberEditSerializer(member,request.data[0])
            if data.is_valid(raise_exception=True):
                data.save()
                return Response("success")
        except Exception as e:
            print ("exzeption is",e)

class Running_Member_List(APIView):
    def get(self,request):
        try:
            profile = authentication(request.META['HTTP_AUTHORIZATION'])
            member = MemberProfile.objects.get(user = profile)
            requestlist = list(RunningChits.objects.filter(member=member).exclude(is_active=False).values_list('chit',flat=True))
            print ("kkkkkkkkkkkkk",requestlist)
            fundcount = len(requestlist)
            chits = Chits.objects.filter(id__in=requestlist, status="RUNNING").order_by('-id')
            chits_dict = chits.values()
            print ("jjjjjjjjjj",chits_dict)
            for idx, chit_dict in enumerate(chits_dict):
                chit_dict['company_logo'] = chits[idx].company_logo.url
                if chits[idx].fixeddepositcopy:
                    chit_dict['fdcopy'] = chits[idx].fixeddepositcopy.url
                if chits[idx].govtissuedcopy:
                    chit_dict['govtcopy'] = chits[idx].govtissuedcopy.url
                run_count = RunningChits.objects.filter(chit=chits[idx],member=member.id,trans_verify=True,foreman=chits[idx].foreman_id).count()

                chit_dict['running_count'] = run_count
            return Response({'data':chits_dict,"fcount":fundcount}, status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class View_dashboard(APIView):
    def get(self,request):
        print("it is hiiiittttttttttt")
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        profile = MemberProfile.objects.filter(user = userid)
        print("@###########################################@@@@@@@@@@@@@@@@",profile)
        if not profile:
            profile = ForemanProfile.objects.filter(id=userid)
            # score = self.updated_gchits_score(request, profile)
            # rating = self.member_star_rating(request, profile)
            # print("RATTTTTTTTTTT++++++++++++", rating)
            return Response('not a user')
        else:
            check = self.check_trans(request, profile)
            print("eeeeeeeeeeeee",check)
            trans_popup = self.auction_transaction_call(request, profile[0].id)
            print("uuuuuuuuuuu",trans_popup)
            score = self.updated_gchits_score(profile)
            rating = self.member_star_rating(profile)
            print("RATTTTTTTTTTT++++++++++++",rating)
            profile[0].member_rating = rating
            serializer = MemberDashboardViewSerializer(profile[0])
            data = {"details":serializer.data,"trans":check,"trans_popup":trans_popup}
            return Response(data,status=status.HTTP_200_OK)
    #
    #
    def updated_gchits_score(self,memdata):
        try:
            print("memmmmmmmmmmmmmmmmmmmmmmm",memdata)
            profile = MemberProfile.objects.get(id = memdata[0].id)
            profile.gchits_score = 0
            print("memberrrrrrrrrrrrrrrrrrrrrrrrrr",profile)
            member_date_of_birth = profile.date_of_birth
            print("DTAEEEEEEEEEEEEEEEEEEEEE",member_date_of_birth)
            current_date = datetime.datetime.now()
            print("evaginnnnnnnnnntimeeeeeeeeeeeee",current_date)
            age = current_date.year - member_date_of_birth.year
            print("givemeeeeeeeeeeeeeeeeeeeeeeee",age)
            if profile.gender == 'Male' and (profile.profession == 'Salaried' or profile.profession == 'Self Employed'):
                profile.gchits_score += 10
            if profile.gender == 'Female':
                profile.gchits_score += 10
            if profile.aadhaar_card:
                profile.gchits_score += 20
            if profile.pancard_number:
                profile.gchits_score += 20
            if profile.qualification == '10th Std':
                profile.gchits_score += 10
            elif profile.qualification == '12th Std':
                profile.gchits_score += 10
            elif profile.qualification == 'Undergraduate':
                profile.gchits_score += 50
            elif profile.qualification == 'Postgraduate':
                profile.gchits_score += 70
            if profile.marital_status == 'Divorcee' and profile.seperated_since == '1 year':
                profile.gchits_score += 10
            elif profile.marital_status == 'Divorcee' and profile.seperated_since == '2 years':
                profile.gchits_score += 30
            elif profile.marital_status == 'Divorcee' and profile.seperated_since == '3 years':
                profile.gchits_score += 40
            elif profile.marital_status == 'Divorcee' and profile.seperated_since == '4+ years':
                profile.gchits_score += 50
            elif profile.marital_status == 'Spouse Deceased':
                profile.gchits_score += 50
            if profile.spouse_work == 'House Maker':
                profile.gchits_score += 10
            elif profile.spouse_work == 'Self Employed':
                profile.gchits_score += 20
            elif profile.spouse_work == 'Salaried':
                profile.gchits_score += 30
            if profile.present_address_type == 'Owned' and profile.profession == 'Salaried':
                profile.gchits_score += 50
            if profile.present_address_type == 'Rented' and profile.profession == 'Salaried':
                profile.gchits_score += 10
            if profile.present_address_type == 'Owned' and profile.profession == 'Self Employed':
                profile.gchits_score += 50
            if profile.present_address_type == 'Rented' and profile.profession == 'Self Employed':
                profile.gchits_score += 20
            if profile.staying_from == 'less than 1 year':
                profile.gchits_score += 10
            elif profile.staying_from == '1 to 3 Years':
                profile.gchits_score += 30
            elif profile.staying_from == '3 to 5 Years':
                profile.gchits_score += 50
            elif profile.staying_from == 'More than 5 Years':
                profile.gchits_score += 70
            if profile.running_two_wheeler_loan == 'Yes':
                profile.gchits_score -= 10
            if profile.running_four_wheeler_loan == 'Yes':
                profile.gchits_score -= 20
            if profile.running_personal_loan == 'Yes':
                profile.gchits_score -= 30
            if profile.running_home_loan == 'Yes':
                profile.gchits_score -= 40
            if profile.running_loans == 'No':
                profile.gchits_score += 110
            if profile.mode_of_salary == 'cash' and profile.profession == 'Salaried':
                profile.gchits_score += 10
            if profile.mode_of_salary == 'bankdeposit' and profile.profession == 'Salaried':
                profile.gchits_score += 100
            if profile.profession == 'Farmer':
                profile.gchits_score += 30
            elif profile.profession == 'Salaried' and profile.are_you_in == 'Government Job':
                profile.gchits_score += 250
            elif profile.profession == 'Salaried' and profile.are_you_in == 'Private Job':
                profile.gchits_score += 150
            elif profile.profession == 'Self Employed' and profile.busines_type == 'Shop Owner':
                profile.gchits_score += 150
            elif profile.profession == 'Self Employed' and profile.busines_type == 'Small Business':
                profile.gchits_score += 50
            if profile.smart_phone == 'Yes':
                profile.gchits_score += 10
            if (age in range(22, 30)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 100
            elif (age in range(31, 35)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 80
            elif (age in range(36, 40)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 60
            elif (age in range(40, 100)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 40
            if (age in range(20, 24)) and profile.marital_status == 'Married':
                profile.gchits_score += 20
            elif (age in range(25, 30)) and profile.marital_status == 'Married':
                profile.gchits_score += 50
            elif (age in range(31, 35)) and profile.marital_status == 'Married':
                profile.gchits_score += 75
            elif (age in range(36, 40)) and profile.marital_status == 'Married':
                profile.gchits_score += 100
            elif (age in range(41, 50)) and profile.marital_status == 'Married':
                profile.gchits_score += 50
            elif (age in range(51, 100)) and profile.marital_status == 'Married':
                profile.gchits_score += 20
            if profile.self_income == '0-2 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 10
            elif profile.self_income == '2-4 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 20
            elif profile.self_income == '4-6 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 30
            elif profile.self_income == '6-10 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 40
            elif profile.self_income == '10-15 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 50
            elif profile.self_income == '15-25 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 100
            elif profile.self_income == '25 L+' and profile.profession == 'Self Employed':
                profile.gchits_score += 150
            if profile.bank_balance == '0-2 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 10
            elif profile.bank_balance == '2-5 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 30
            elif profile.bank_balance == '5-10 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 50
            elif profile.bank_balance == '10-25 L' and profile.profession == 'Self Employed':
                profile.gchits_score += 70
            elif profile.bank_balance == '25 L+' and profile.profession == 'Self Employed':
                profile.gchits_score += 100
            if (age in range(22, 30)) and profile.marital_status == 'Unmarried':
                print("222222222222222222222")
                profile.gchits_score += 100
                print("profileeeeeeeeeeee3333@@@@@@@@", profile.gchits_score)
            elif (age in range(31, 35)) and profile.marital_status == 'Unmarried':
                print("4444444444444444444444")
                profile.gchits_score += 80
            elif (age in range(36, 40)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 60
            elif (age in range(40, 100)) and profile.marital_status == 'Unmarried':
                profile.gchits_score += 40
            print("profileeeeeeeeeeee3333@@@@@@@@",profile.gchits_score)
            profile.save()
            print("555555555554444444444444",profile.gchits_score)

            return profile.gchits_score
        except Exception as e:
            print("555555555554444444444444",e)
            return "failed"


    def member_star_rating(self ,memdata):

        profile = MemberProfile.objects.get(id=memdata[0].id)

        if profile.gchits_score <= 500:
            profile.member_rating = 0
        else:
            profile.member_rating = 1
        if profile.cibil_score <= 500:
            profile.member_rating += 1
        elif (profile.cibil_score > 500 and profile.cibil_score <= 600):
            profile.member_rating += 2
        elif (profile.cibil_score > 600 and profile.cibil_score <= 700):
            profile.member_rating += 3
        else:
            profile.member_rating += 4
        profile.save()
        return profile.member_rating


    def check_trans(self,request,profile):
        run = RunningChits.objects.filter(member=profile[0].id, transcationid=None)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#",run)
        check = []
        if run:
            for i in run:
                print("iiiiiiiiiiii",i)
                id1 = i.chit
                print("22222222222",id1)
                runningcount = i.member_count;
                count_id = RunningChits.objects.filter(chit=id1, is_active=True).count()
                chit = Chits.objects.filter(id=id1)
                print("etttttttttt",chit)
                foreman1 = i.foreman
                foreman = ForemanProfile.objects.filter(id=foreman1)
                foremanaccountnumber = foreman[0].account_number
                foremanbankname = foreman[0].bank_name
                foremanbankbranch = foreman[0].branch_name
                foremanbankifsc = foreman[0].ifsc_code
                foremanaccountname = foreman[0].account_name
                amount = chit[0].chit_amount / chit[0].chit_duration
                chit_name = chit[0].chit_number
                chit_id = chit[0].id
                leftmembers = chit[0].chit_duration - count_id
                if count_id == chit[0].chit_duration:
                    data = {"res": "True", "amount": amount, "chitname": chit_name, "chit_id": chit_id,
                            "foremanaccountnumber": foremanaccountnumber, "foremanbankname": foremanbankname,
                            "foremanbankbranch": foremanbankbranch, "foremanbankifsc": foremanbankifsc,
                            "foremanaccountname": foremanaccountname, "count": runningcount}
                else:
                    data = {"res": "False", "chitname": chit_name, "chit_id": chit_id, "left members": leftmembers}
                check.append(data)
            return check
        else:
            data = "no data found"
            check.append(data)
            return check

    def auction_transaction_call(self,request, profile):
        run = list(RunningChits.objects.filter(member=profile, is_active=True).values('chit', 'member_count'))
        print("ruuuuuuuuu",run)
        details = []
        for i in run:
             final = FinalAuctions.objects.filter(chit=i['chit']).exclude(member=None, foreman=None,
                                                                          bid_amount=None).count()
             print("fiiiiiiiiii222222222222",final)
             if Q(final == 0) | Q(final == int(final) + 1):
                 final1 = FinalAuctions.objects.filter(chit=i['chit'], auction_count=int(final) + 1)
                 print("9999999999",final1)
                 trans = Transactions.objects.filter(chit=i['chit'], auction=int(final) + 1, member=profile,
                                                     mem_count=i['member_count']).exclude(transaction_id=None)
                 print("transssssss",trans)
                 if not trans:
                     if final1:
                         date1 = final1[0].auctiondate
                         print("yyyyyyyyyyyy",i['chit'])
                         chitname = Chits.objects.filter(id=i['chit'])
                         print("uuuuuuuuuuuuuuu",chitname)
                         chit_name = chitname[0].chit_number
                         premium_amount = final1[0].payable_amount
                         auction = final1[0].auction_count
                         currentdate = datetime.datetime.now().replace(microsecond=0)
                         date2 = date1 + relativedelta(days=-1)
                         date3 = date1 + relativedelta(days=-3)
                         date4 = date1 + relativedelta(hours=+1)
                         revise1 = str(date4)[:16]
                         revise2 = str(date2)[:16]
                         var = str(currentdate)[:16]
                         var1 = str(date3)[:16]
                         var2 = str(date2)[:16]
                         if var1 <= var <= revise2:
                             res = True
                         elif var2 <= var <= revise1:
                             res = 'CLOSE'
                         else:
                             res = False
                         final2 = FinalAuctions.objects.filter(chit=i['chit'], auction_count=final)
                         foreman = ForemanProfile.objects.filter(id=chitname[0].foreman)
                         foremanaccountnumber = foreman[0].account_number
                         foremanbankname = foreman[0].bank_name
                         foremanbankbranch = foreman[0].branch_name
                         foremanbankifsc = foreman[0].ifsc_code
                         foremanaccountname = foreman[0].account_name
                         if not final:
                             data = {"chitname": chit_name, "auction": auction, "res": res, "chit_id": i['chit'],
                                     "amount": premium_amount, "foremanaccountnumber": foremanaccountnumber,
                                     "foremanbankname": foremanbankname,
                                     "foremanbankbranch": foremanbankbranch, "foremanbankifsc": foremanbankifsc,
                                     "foremanaccountname": foremanaccountname, "membercount": i['member_count']}

                         else:
                             payable_amount = final2[0].payable_amount
                             data = {"chitname": chit_name, "auction": auction, "res": res, "chit_id": i['chit'],
                                     "amount": payable_amount, "foremanaccountnumber": foremanaccountnumber,
                                     "foremanbankname": foremanbankname,
                                     "foremanbankbranch": foremanbankbranch, "foremanbankifsc": foremanbankifsc,
                                     "foremanaccountname": foremanaccountname, "membercount": i['member_count']}
                         details.append(data)
                     else:
                         data = False
                         details.append(data)
                 else:
                     data = False
                     details.append(data)
             else:
                 data = False
                 details.append(data)
        return details


class MemberTransaction(APIView):
    def post(self,request):
        user = authentication(request.META['HTTP_AUTHORIZATION'])
        user_id = MemberProfile.objects.get(user = user)
        print("$$$$$$$$$$$$",request.data)
        chitid = request.data['chitid']
        membercount = request.data['chitcount']
        transaction1 = request.data['transid']
        chit = Chits.objects.filter(id=chitid)
        run = RunningChits.objects.filter(chit=chitid, member=user_id, is_active=True,
                                          member_count=membercount).update(transcationid=transaction1,
                                                                                      depdate=datetime.datetime.
                                                                                      now().date())
        run1 = list(RunningChits.objects.filter(chit=chitid).exclude(transcationid=None).values_list('member', flat=True))
        run2 = len(run1)
        value = chit[0].chit_duration - run2
        memlist = []
        if run2 == chit[0].chit_duration:
             for i in run1:
                 j = str(i)
                 member = MemberProfile.objects.filter(id=j)
                 token1 = str(member[0].device_token)
                 memlist.append(token1)
                 data = {"res": "chit auction will be conduct after 30 days", "membertoken": memlist}
        else:
             member = MemberProfile.objects.filter(id=user_id)
             token1 = str(member[0].device_token)
             memlist.append(token1)
             res = str(value) + " " + "members have to deposite money to start auction"
             data = {"res": res, "membertoken": memlist}
        return Response(data)

class AuctionTransactions(APIView):
    def post(self,request):
        print("9999999999",request.data)
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        member = MemberProfile.objects.get(user=userid)
        chits = Chits.objects.filter(id=request.data['chitid'])
        trans = Transactions()
        trans.member = member
        trans.chit = request.data['chitid']
        trans.transaction_id = request.data['trans']
        trans.auction = request.data['auctioncount']
        trans.mem_count = request.data['chitcount']
        trans.foreman = chits[0].foreman
        trans.trans_date = datetime.datetime.now()
        trans.paid_amount =request.data['paidAmount']
        trans.save()
        return Response('Trasaction Id Saved Successfully')

class FundRunningDetails(APIView):
    def post(self,request):
        print("reeeeeeeeeeeeee222222222222222222",request.data)
        id = authentication((request.META['HTTP_AUTHORIZATION']))
        member = MemberProfile.objects.get(user = id)
        chit_id = request.data['id']
        details = []
        chitinfo = Chits.objects.filter(id=chit_id)
        total_amount = chitinfo.values()
        print("tooooooooo",total_amount,chit_id)
        finalcount = total_amount[0]['chit_duration']
        print("6666666666$$$$$$$$$",finalcount,type(finalcount))
        Foreman_comission = chitinfo.values_list('foreman_commission', flat=True)
        auction1 = FinalAuctions.objects.filter(chit=chit_id).order_by('auctiondate')
        # temp = list(auction1)
        refchit = Chits.objects.filter(id=chit_id).values('chit_amount', 'foreman_id')[0]
        # total_chit_amount = refchit['chit_amount']
        foreman_id = refchit['foreman_id']
        print("Foreman_comission auction1 refchit foreman_id",Foreman_comission,auction1, refchit, foreman_id)
        for i in auction1:
            if (i.foreman == None) or (i.member == None):
                comission = 0
                # prize_money = float(total_chit_amount) - float(i.default_bid_amount)
                mem_name = "GFUNDS"
                fore_name = "None"
                prize_money = float(i.default_chit_amount) - float(i.default_bid_amount)
                bid_amount = i.default_bid_amount
                payable_amount = 0
                aucdate = str(i.auctiondate)[:10]
                Foremancomission = Foreman_comission[0]
            else:
                if (int(i.auction_count)) < finalcount:
                    temp1 = int(i.auction_count) + 1
                    nextpay = FinalAuctions.objects.filter(auction_count=temp1, chit=chit_id).values('payable_amount')
                    payable_amount = nextpay[0]['payable_amount']
                else:
                    payable_amount = 0

                comission = i.foreman_platform_comission
                mem = MemberProfile.objects.filter(id=i.member)
                mem_name = mem[0].full_name
                fore = ForemanProfile.objects.filter(id=foreman_id)
                fore_name = fore[0].full_name
                prize_money = i.receiving_member_amount
                bid_amount = i.bid_amount
                aucdate = str(i.auctiondate)[:10]
                Foremancomission = Foreman_comission[0]

            if total_amount[0]['chit_type'] == "Fixed Duration":
                final = FinalAuctions.objects.filter(chit=chit_id).values_list('auction_count', flat=True)
                maxauction = max(final)
                balance1 = FinalAuctions.objects.filter(chit=chit_id, auction_count=i.auction_count).values()
                dur = Chits.objects.get(id=chit_id)
                div = balance1[0]['balance_amount'] / dur.chit_duration
                divident_value = int(div)
                data = {"member": mem_name, "foreman": fore_name, "date": aucdate, "bidamount": bid_amount,
                        "nextpayableamount": payable_amount, "auctioncount": i.auction_count, "commission": comission,
                        "prizemoney": prize_money, "Foremancomission": Foremancomission,
                        "balance_amount": i.balance_amount,"chit_number":chit_id,
                        "dividend_value": divident_value, "next_date": i.next_date,
                        "member_id": balance1[0]['member']}
                details.append(data)

        # a = FinalAuctions.objects.filter(chit=request.data['id']).values('auctiondate').first()
        details={'details':details}
        return Response(details)

class TransactionRecord(APIView):
    def post(self,request):
        mem_id = authentication(request.META['HTTP_AUTHORIZATION'])
        finalData1 =Transactions.objects.none()
        final1 = []
        member = MemberProfile.objects.get(user=mem_id)
        Status = request.data['status']
        if Status == 'RUNNING' :
            try:
                memdata = RunningChits.objects.filter(member=member).values_list('chit',flat=True)
                memdata2 =list(map(lambda x: Chits.objects.filter(Q(status= Status) | Q(status='CLOSED'),id=x).values('id','chit_number'),memdata))
                for i in range(len(memdata2)):
                    finalData1 = finalData1 | memdata2[i]
                for i in finalData1:
                    for j in Transactions.objects.filter(chit=i['id'],member = member).values():
                        j['chitName']=i['chit_number']
                        j['trans_date']=str(j['trans_date'])[:10]
                        final1.append(j)
            except:
                data = "No Chits Found"
            return Response(final1)

        # mem_id = authentication(request.META['HTTP_AUTHORIZATION'])
        # print ("memmmmmmmmmiddddddd",mem_id)
        # member = MemberProfile.objects.get(user=mem_id)
        # status1 = request.data['status']
        # print("staaaaaaaaaa",status1)
        # if status1 == 'RUNNING':
        #     print("insideeeeee idfffffffffffffffffffffff")
        #     try:
        #         memdata = RunningChits.objects.filter(member=member).values_list('chit', flat=True)
        #         print("chiiiiiiii", memdata)
        #         data = map(lambda x: Chits.objects.filter(status=status1, id=x).values('id', 'company_logo', 'chit_number'),set(memdata))
        #         print("daaaaaaaaaaaaaaaaaaattttttttttaaaaaaaaaaaaaaaaaa", data)
        #         data2 = filter(lambda x: len(x) != 0, data)
        #         count1 = len(data2)
        #         if count1 == 0:
        #             data1 = 'No Data Found'
        #         else:
        #             data1 = data2
        #     except:
        #         data = "No Chits Found"
        #
        #     return Response(data2)
        #
        # elif status1 == '':
        #     amount = MemberProfile.objects.filter(id = member).values('id','account_number')
        #     print("amouttttttttttttttttttt",amount)
        #     trans = FinalAuctions.objects.filter(chit = request.data['data2']).values('payable_amount','auction_count')
        #     print("transssssssssssssssssssssss",trans)
        #     chit = Chits.objects.filter(id = request.data['data2']).values()
        #     print("ccccccccccccccccccccccc",chit)
        #     duration = chit[0]['chit_duration']
        #     logo = chit[0]['company_logo']
        #     print("durrrrrrrrrrrrrrr",duration)
        #     for i in range(1,int(duration) + 1):
        #         trans = Transactions.objects.filter(chit = request.data['data2'], member = member,mem_count=request.data['count']).values('member','chit','foreman','auction','trans_date')
        #         print("t111111111111111",trans)
        #         if trans:
        #             details = trans.values()
        #             # data3 = filter(lambda x: len(x != 0),details)
        #             for i in details:
        #                 print("hhhhhhhhhhhhhhhhh",i)
        #                 i['account_number'] = amount[0]['account_number']
        #                 i['company_logo'] = logo
        #             return Response(details)
        #         else:
        #             return Response("No transactions")
        # else:
        #     data = RunningChits.objects.filter(member=member,chit=request.data['data2']).values('member_count','chit').order_by('id')
        #     return Response(data)

class AuctionTime(APIView):
    def post(self,request):
        # print ("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",request.data)
        chit = request.data['id']

        final = FinalAuctions.objects.filter(chit=chit).exclude(flag = False).count()
        print("COUNTTTTTTTTTT",final)
        count1 = int(final) + 1
        final1 = FinalAuctions.objects.filter(chit=chit, auction_count=count1)
        print("yyyyyyyyyyyyy",final1)
        trans = list(Transactions.objects.filter(chit=chit).values_list('auction', flat=True).distinct())
        trans1 = map(str, trans)
        res = ''
        if str(count1) in trans1:
            check_count = Transactions.objects.filter(chit=chit, auction=count1, check=True).count()
            chit = Chits.objects.filter(id=chit)
            if check_count == (chit[0].chit_duration):

                res = True
            else:
                print("elseeeeeeee 777777777")
                res = False
        response = res
        print("5555555555555555",response)
        if final1[0]:
            date1 = final1[0].auctiondate
        # data1 = str(date1)[:16]
        today1 = str(datetime.datetime.now())
        print ("::::::::::::::::::::::::",date1)
        data = {"date": date1, "res": response, "today": today1}
        print("JJJJJJJJJJJJJ",data)
        return Response(data)




class Check_Repeated_Auction(APIView):
    def post(self,request):
        print("sssssssssssss",request.data)
        chit_id = request.data['id']
        data = 'emptystring'
        gettodaymonth = str(datetime.date.today())[5:7]
        gettodaydate = str(datetime.date.today())[8:11]
        gettodayyear = str(datetime.date.today())[:4]
        try:
            with transaction.atomic():
                print("basssssssssu")
                check_final = FinalAuctions.objects.get(chit=chit_id,
                                                        flag=False,auctiondate__month=gettodaymonth,
                                                        auctiondate__day=gettodaydate,
                                                        auctiondate__year=gettodayyear)
                currentdate = datetime.datetime.now()
                splitdate = datetime.datetime.strftime(currentdate, "%Y-%m-%d")
                finaldate = datetime.datetime.strptime(splitdate, "%Y-%m-%d")
                stringdate = datetime.datetime.strftime(check_final.auctiondate, "%Y-%m-%d")
                databasedate = datetime.datetime.strptime(stringdate, "%Y-%m-%d")
                if check_final.flag == False:
                    check_final.flag = True
                    check_final.save()
                    if finaldate.date() == databasedate.date():
                        flagfinal = True
                    else:
                        data = "check_final failure", chit_id
                        flagfinal = False
                    if flagfinal == True:
                        data = approve_auction(chit_id)
                        print("sannnnnnnnnnn",data)
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)




def approve_auction(chit_id):
    print("chitiddddddddddd",chit_id)
    chit = Chits.objects.filter(id=chit_id)
    foreman_id = chit[0].foreman
    # chit_amount = int(chit[0].chit_amount)
    chit_type = chit[0].chit_type
    foreman_commission = int(chit[0].foreman_commission)
    chit_duration = int(chit[0].chit_duration)
    print("foreman idddddddd, chit_type, foreman_commission, chit_duration",foreman_id, chit_type,foreman_commission, chit_duration)

    extra_charges = foreman_commission
    count = FinalAuctions.objects.filter(chit=chit_id).exclude(bid_amount=None)
    count1 = count.count()
    count2 = int(count1) + 1
    date = FinalAuctions.objects.filter(auction_count=count2, chit=chit_id)
    default_bidamount1 = FinalAuctions.objects.filter(auction_count=count2, chit=chit_id).values()
    print("default_bidamount1vvvvvvvvvvvvvvvvvvv",default_bidamount1,date, count1, count2)
    chit_amount = int(default_bidamount1[0]['default_chit_amount'])
    default_bidamount =int(default_bidamount1[0]['default_bid_amount'])
    auctiondate1 = date[0].auctiondate
    premium_amount = chit_amount / chit_duration
    foreman_platform_comission = (chit_duration * 100) * (0.4)
    print("chit_amount,default_bidamount,auctiondate1,premium_amount, foreman_platform_comission",chit_amount,default_bidamount,auctiondate1,premium_amount,foreman_platform_comission)

    # foreman_referral = Resellers_Referel.objects.filter(foreman_id_id=foreman_id)
    # if foreman_referral:
    #     reseller_comission = (chit_duration * 100) * (0.2)
    #     platform_comission = (chit_duration * 100) * (0.4)
    # else:
    #     reseller_comission = 0
    #     platform_comission = (chit_duration * 100) * (0.6)

    if chit_type == 'Fixed Duration':
        auct = Auctions.objects.filter(chit=chit_id).count()
        print("aucttttttttttttt",auct)
        if auct != 0:
            print("666666########## auct != 0 auct != 0 auct != 0")
            temp = Auctions.objects.filter(chit=chit_id).order_by('-bid_amount')[0]
            max_amount = temp.bid_amount
            print("9999999993333 max_amount max_amount",max_amount,chit_amount)
            mem_list = Auctions.objects.filter(chit=chit_id, bid_amount=max_amount).order_by('auction_call_date')[0]
            print("membeeeeeeeeeee",mem_list)
            receiving_member_id = mem_list.member
            left_amount = max_amount - extra_charges
            next_payable_amount = premium_amount - (left_amount/chit_duration)
            receiver_amount = chit[0].chit_amount-max_amount
            membercounts =list(RunningChits.objects.filter(chit=chit_id,member=receiving_member_id).values_list('member_count',flat=True))
            print("mem couuuuuu",membercounts)
            finalmemcount = list(FinalAuctions.objects.filter(chit=chit_id,member=receiving_member_id).values_list('member_count',flat=True))
            print("finallllll mmmmmmmmm",finalmemcount)
            list1 = map(lambda x:str(x),membercounts)
            list2 = map(lambda x:str(x),finalmemcount)
            set1 = set(list1)
            set2 = set(list2)
            finalset = set1.difference(set2)
            counts = list(finalset)
            print("list1 list1 list2 list2 finalset finalset countscounts",list1, list2,set1,set2,finalset,counts)
            FinalAuctions.objects.filter(auction_count=count2, chit=chit_id )\
                .update(bid_amount=max_amount,
                        payable_amount=next_payable_amount,
                        receiving_member_amount=receiver_amount,
                        foreman_platform_comission=foreman_platform_comission,
                        # platform_comission=platform_comission,
                        balance_amount=max_amount-foreman_commission
                        )
            # update_foreman_deposit(platform_comission, foreman_id)
            Auctions.objects.filter(chit=chit_id).delete()
            check_closed_chit(chit_id)
            print("llllllllll999999")
            mem_data = MemberProfile.objects.filter(id=receiving_member_id).values('full_name')
            print("finllllllllll data",mem_data)
            data = {'full_name': mem_data[0]['full_name'], 'bid_amount': max_amount, 'prize_money': receiver_amount}
            print("9999999999999999999999999sach")
            return data
        else:
            running = list(RunningChits.objects.filter(chit=chit_id).values_list('member', flat=True).distinct())
            final = list(FinalAuctions.objects.filter(chit=chit_id).values_list('member', flat=True).exclude(member=None))
            set_running = set(running)
            set_final = set(final)
            list1 = set_running ^ set_final
            list2 = map(str, list1)
            member = (random.choice(list2))
            receiving_member_id = member
            print("running , final, set_running, set_final, list1, list2, member, receiving_member_id",running, final, set_running, set_final, list1, list2,member,receiving_member_id)
            # receiver_amount = chit_amount-extra_charges
            receiver_amount = chit_amount-default_bidamount
            left_amount = default_bidamount - extra_charges
            next_payable_amount = premium_amount - (left_amount / chit_duration)
            balance_amount = left_amount
            FinalAuctions.objects.filter(auction_count=count2, chit=chit_id).update(
                                                                      bid_amount=default_bidamount,
                                                                      payable_amount=next_payable_amount,
                                                                      receiving_member_amount=receiver_amount,
                                                                      foreman_platform_comission=foreman_platform_comission,
                                                                      # platform_comission=platform_comission,
                                                                      # reseller_comission=reseller_comission,
                                                                      balance_amount=balance_amount)
            # update_foreman_deposit(platform_comission, foreman_id)
            Auctions.objects.filter(chit=chit_id).delete()
            check_closed_chit(chit_id)
            mem_data = MemberProfile.objects.filter(id=receiving_member_id).values('full_name')
            data = {'full_name': mem_data[0]['full_name'], 'bid_amount': default_bidamount, 'prize_money': receiver_amount}
            print ("aut !!!!!!!!!!!!!=0 dataaaaaaaaaaaaaaaaa",data)
            return data
    else:
        auct1 = Auctions.objects.filter(chit=chit_id).count()
        if auct1 != 0:
            final = FinalAuctions.objects.filter(chit=chit_id).exclude(bid_amount=None).count()
            temp = Auctions.objects.filter(chit=chit_id).order_by('-bid_amount')[0]
            max_amount = temp.bid_amount
            mem_list = Auctions.objects.filter(chit=chit_id, bid_amount=max_amount).order_by('auction_call_date')[0]
            receiving_member_id = mem_list.member
            left_amount = max_amount - extra_charges
            if final == 0:
                bal_amount = left_amount
            else:
                balance = FinalAuctions.objects.filter(chit=chit_id, auction_count=final)
                bal_amount = int(balance[0].balance_amount) + int(left_amount)
            next_payable_amount = premium_amount
            receiver_amount = chit_amount - max_amount
            FinalAuctions.objects.filter(auction_count=count2, chit=chit_id).update(member=receiving_member_id,
                                                                                    foreman=foreman_id.id,
                                                                                    bid_amount=max_amount,
                                                                                    payable_amount=next_payable_amount,
                                                                                    receiving_member_amount=receiver_amount,
                                                                                    foreman_platform_comission=foreman_platform_comission,
                                                                                    # platform_comission=platform_comission,
                                                                                    # reseller_comission=reseller_comission,
                                                                                    balance_amount=bal_amount,
                                                                                    )
            # update_foreman_deposit(platform_comission, foreman_id)
            check_closed_chit(chit_id)
            final1 = FinalAuctions.objects.filter(chit=chit_id).exclude(bid_amount=None).count()
            balance1 = FinalAuctions.objects.filter(chit=chit_id, auction_count=final1)
            Auctions.objects.filter(chit=chit_id, bid_amount=max_amount).order_by('auction_call_date')[0].delete()
            temp1 = list(Auctions.objects.filter(chit=chit_id).values_list('bid_amount', flat=True))
            # listtemp1 = map(str, temp1)
            if len(temp1) != 0:
                receiving_member_id1 = None
                temp1 = Auctions.objects.filter(chit=chit_id).order_by('-bid_amount')[0]
                max_amount1 = temp1.bid_amount
                mem_list1 = Auctions.objects.filter(chit=chit_id, bid_amount=max_amount1).order_by('auction_call_date')[0]
                final_balance_amount = balance1[0].balance_amount
                print("aaaaaaaa",final_balance_amount,chit_amount,max_amount1,default_bidamount)
                if int(final_balance_amount) > int(int(chit_amount)-int(max_amount1)+int(default_bidamount)):
                    receiving_member_id1 = mem_list1.member
                    next_payable_amount = premium_amount
                    receiver_amount1 = chit_amount - max_amount1
                    bal_amount2 = int(final_balance_amount)-int(receiver_amount1)-int(default_bidamount)
                    FinalAuctions.objects.filter(auction_count=int(count2)+1, chit=chit_id).update(member=receiving_member_id1,
                                                                                            foreman=foreman_id.id,
                                                                                            bid_amount=max_amount1,
                                                                                            payable_amount=next_payable_amount,
                                                                                            receiving_member_amount=receiver_amount1,
                                                                                            foreman_platform_comission=foreman_platform_comission,
                                                                                            # platform_comission=platform_comission,
                                                                                            # reseller_comission=reseller_comission,
                                                                                            balance_amount=bal_amount2,
                                                                                            auctiondate=auctiondate1)
                day = int(auctiondate1.strftime("%d"))
                for i in range(count2 + 2, int(chit_duration) + 1):
                    FinalAuctions.objects.filter(auction_count=i, chit=chit[0].id).update(
                        auctiondate=auctiondate1 + relativedelta(days=day - 1),
                        next_date=auctiondate1 + relativedelta(days=day))
                    day = day + 1
                # update_foreman_deposit(platform_comission, foreman_id)
                Auctions.objects.filter(chit=chit_id).delete()
                check_closed_chit(chit_id)
                mem_data = MemberProfile.objects.filter(id__in=[receiving_member_id, receiving_member_id1])\
                    .values('full_name')
                data = [{'full_name': mem_data[0]['full_name'], 'bid_amount': max_amount,
                         'prize_money': receiver_amount}, {'full_name': mem_data[1]['full_name'],
                                                           'bid_amount': max_amount1, 'prize_money': receiver_amount1}]
                return data
            else:
                final_balance_amount = balance1[0].balance_amount
                if int(final_balance_amount) > int(int(chit_amount) - int(default_bidamount)):
                    running = list(RunningChits.objects.filter(chit=chit_id).values_list('member', flat=True).distinct())
                    final = list(
                        FinalAuctions.objects.filter(chit=chit_id).values_list('member', flat=True).exclude(member=None))
                    set_running = set(running)
                    set_final = set(final)
                    list1 = set_running ^ set_final
                    # list2 = map(str, list1)
                    member = (random.choice(list1))
                    receiving_member_id1 = member
                    receiver_amount1 = chit_amount - default_bidamount
                    next_payable_amount = premium_amount
                    final_balance_amount = int(balance1[0].balance_amount) - int(receiver_amount)
                    FinalAuctions.objects.filter(auction_count=int(count2)+1, chit=chit_id).update(member=receiving_member_id1,
                                                                                            foreman=foreman_id.id,
                                                                                            bid_amount=default_bidamount,
                                                                                            payable_amount=next_payable_amount,
                                                                                            receiving_member_amount=receiver_amount1,
                                                                                            foreman_platform_comission=foreman_platform_comission,
                                                                                            # platform_comission=platform_comission,
                                                                                            # reseller_comission=reseller_comission,
                                                                                            balance_amount=final_balance_amount)
                    # update_foreman_deposit(platform_comission, foreman_id)
                    Auctions.objects.filter(chit=chit_id).delete()
                    check_closed_chit(chit_id)
                    # mem_data = MemberProfile.objects.filter(id=receiving_member_id).values('full_name')
                    # data = {'full_name': mem_data[0]['full_name'], 'bid_amount': extra_charges,
                    #         'prize_money': receiver_amount}
                    mem_data = MemberProfile.objects.filter(id__in=[receiving_member_id, receiving_member_id1]) \
                        .values('full_name')
                    data = [{'full_name': mem_data[0]['full_name'], 'bid_amount': max_amount,
                             'prize_money': receiver_amount}, {'full_name': mem_data[1]['full_name'],
                                                               'bid_amount': default_bidamount,
                                                               'prize_money': receiver_amount1}]
                    return data
        else:
            final4 = FinalAuctions.objects.filter(chit=chit_id).exclude(bid_amount=None).count()
            if final4 == 0:
                bal_amount = 0
            else:
                balance = FinalAuctions.objects.filter(chit=chit_id, auction_count=final4)
                bal_amount = balance[0].balance_amount
            running = list(RunningChits.objects.filter(chit=chit_id).values_list('member', flat=True).distinct())
            final = list(
                FinalAuctions.objects.filter(chit=chit_id).values_list('member', flat=True).exclude(member=None))
            set_running = set(running)
            set_final = set(final)
            list1 = set_running ^ set_final
            # list2 = map(str, list1)
            member = (random.choice(list1))
            receiving_member_id = member
            receiver_amount = chit_amount - default_bidamount
            next_payable_amount = premium_amount
            FinalAuctions.objects.filter(auction_count=count2, chit=chit_id).update(member=receiving_member_id,
                                                                                    foreman=foreman_id.id,
                                                                                    bid_amount=default_bidamount,
                                                                                    payable_amount=next_payable_amount,
                                                                                    receiving_member_amount=receiver_amount,
                                                                                    foreman_platform_comission=foreman_platform_comission,
                                                                                    # platform_comission=platform_comission,
                                                                                    # reseller_comission=reseller_comission,
                                                                                    balance_amount=bal_amount)
            # update_foreman_deposit(platform_comission, foreman_id)
            Auctions.objects.filter(chit=chit_id).delete()
            check_closed_chit(chit_id)
            mem_data = MemberProfile.objects.filter(id=receiving_member_id).values('full_name')
            data = {'full_name': mem_data[0]['full_name'], 'bid_amount': default_bidamount,
                    'prize_money': receiver_amount}
            return data


def update_foreman_deposit(platform_comission,foreman_id):
    foreman_details = ForemanProfile.objects.get(id=foreman_id)
    ForemanProfile.objects.filter(id=foreman_id).update(foreman_deposit_amount=(float(foreman_details.foreman_deposit_amount)-platform_comission))
    return "updated successfully"



def check_closed_chit(chit_id):
    final = FinalAuctions.objects.filter(chit=chit_id).exclude(bid_amount=None, member=None, foreman=None).count()
    chit = Chits.objects.get(id=chit_id)
    duration = chit.chit_duration
    if duration == final:
            Chits.objects.filter(id=str(chit)).update(status='CLOSED')
            print("ssssssssss")
            return 'Status Changed to Closed'

    else:
        return 'chit is in running status'


class MemberAuctionalloted(APIView):
    def get(self,request):
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        mem_id = MemberProfile.objects.get(user = id)
        uniqueFunds = []
        print("aaaaaaaaaaaaaaaaaaaa",mem_id)
        try:
            memdata = FinalAuctions.objects.filter(member = mem_id).values('auction_count','auctiondate','member','receiving_member_amount',
                                                                 'chit','bid_amount','foreman_transaction',
                                                                  'foreman_transaction_status').order_by("chit")
            for ch in memdata:
                fundimg = Chits.objects.filter(id=ch['chit'])
                ch['chit_name'] = fundimg[0].company_name
                ch['company_logo'] = fundimg[0].company_logo.url
                uniqueFunds.append(ch)
                chCount = 0
                for uni in uniqueFunds:
                    if (ch["chit"] == uni["chit"]):
                        chCount += 1
                        if (chCount > 1):
                            uniqueFunds.remove(uni)
            return Response(uniqueFunds)
        except Exception as e:
            print(e)
            return Response("FAILEDDDDD")


class Closedfunds(APIView):
    def get(self,request):
        try:
            profile = authentication(request.META['HTTP_AUTHORIZATION'])
            print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",profile)
            profile=MemberProfile.objects.get(user_id=profile)
            print(profile)
            requests = list(Request.objects.filter(member_id=profile).values_list('chit_id', flat=True))
            print (requests)
            chits = Chits.objects.filter(status="CLOSED").order_by('-id')
            chit_count = Chits.objects.filter(status="CLOSED").count()
            chits_dict = chits.values()
            for idx, chit_dict in enumerate(chits_dict):
                chit_dict['company_logo'] = chits[idx].company_logo.url
            return Response({'data': chits_dict, 'chit_count': chit_count}, status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MemberHomegraph(APIView):
    def get(self, request):
        try:
            final_data = []
            results = []
            count = 0
            profile = authentication(request.META['HTTP_AUTHORIZATION'])
            # da = MemberProfile.objects.get(user_id=profile)
            try:
                da1 = ForemanProfile.objects.get(user_id=profile)
                profile = da1
                chits = Chits.objects.filter(foreman=str(da1), status='RUNNING').values_list('id', flat=True).last()
            except ForemanProfile.DoesNotExist as e:
                da = MemberProfile.objects.get(user_id=profile)
                profile = da
                chits = Chits.objects.filter( status='RUNNING').values_list('id', flat=True).last()

            if not chits:
                running_chits = RunningChits.objects.filter(member=profile).values_list('chit', flat=True).last()
                chits = Chits.objects.filter(id=int(running_chits), status='RUNNING').values_list('id', flat=True)

                final_auctions = FinalAuctions.objects.filter(chit=chits[0]) \
                    .values('chit', 'bid_amount', 'receiving_member_amount', 'auctiondate', 'default_bid_amount',
                            'default_chit_amount')
                expected_values = FinalAuctions.objects.filter(chit=chits[0])
            else:
                final_auctions = FinalAuctions.objects.filter(chit=chits, foreman__isnull=False) \
                    .values('chit', 'bid_amount', 'receiving_member_amount', 'auctiondate', 'default_bid_amount',
                            'default_chit_amount')
                expected_values = FinalAuctions.objects.filter(chit=chits)
            for i in expected_values:
                expected_data = {}
                temp = "value0"
                serializer = FinalAuctionsViewSerializer(i)
                fullexpectedserializer = serializer.data
                fullexpectedserializer.update(
                    {'receiving_member_amount': int(i.default_chit_amount) - int(i.default_bid_amount)})
                expected_data[temp] = fullexpectedserializer['receiving_member_amount']
                expected_data['chit'] = fullexpectedserializer['chit']
                print(fullexpectedserializer['auctiondate'])
                expected_data['finaldate'] = fullexpectedserializer['auctiondate']
                expected_data['date'] = expected_data['finaldate'][0:10]
                final_data.append(expected_data)
            if final_auctions:
                print("hiiiiiiiiiiii")
                prev_data = final_auctions[0]
                dict_data = {}
                temp = "value1"
                for final in final_auctions:
                    # print("finaaaaaaaaaaaaaa",final)
                    if final['chit'] not in prev_data.values():
                        count += 2
                        temp = "value" + str(count)


                    results.append(final)
                    print("rqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",results)
            sorted_data = sorted(final_data, key=itemgetter('date'))
            real_sort = sorted(results,key = lambda i:i['auctiondate'])
            return Response({"chit_data": sorted_data, "chit_count": count,'real_data':real_sort}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)







# class MemberHomegraph(APIView):
#     def get(self,request):
#
#
#         try:
#             final_data = []
#             count = 0
#             profile = authentication(request.META['HTTP_AUTHORIZATION'])
#             print("%%55%%%%%%%555555555",profile)
#             try:
#                 profile = ForemanProfile.objects.get(user_id=profile)
#                 chits = Chits.objects.filter(foreman=str(profile), status='RUNNING').values_list('id', flat=True).last()
#             except ForemanProfile.DoesNotExist as e:
#                 profile = MemberProfile.objects.get(user_id=profile)
#                 print("chal chaiya chiya",profile)
#                 chits = Chits.objects.filter(foreman=str(profile), status='RUNNING').values_list('id', flat=True).last()
#                 print("vvvvvvvvvvvvvvv",chits)
#
#             if not chits:
#                 print("print inside chits")
#                 running_chits = RunningChits.objects.filter(member=profile).values_list('chit', flat=True).last()
#                 print("bbbbbbbbbb",running_chits,type(running_chits))
#                 chits = Chits.objects.filter(id=int(running_chits), status='RUNNING').values_list('id', flat=True)
#                 print("LLLLLLLLL",chits[0])
#                 final_auctions = FinalAuctions.objects.filter(chit=chits[0], foreman__isnull=False) \
#                     .values('chit', 'bid_amount', 'receiving_member_amount', 'auctiondate', 'default_bid_amount',
#                             'default_chit_amount')
#                 print("finallllllllllllaction",final_auctions)
#                 expected_values = FinalAuctions.objects.filter(chit=chits[0])
#                 print("expected_values", expected_values.values())
#             else:
#                 print("inside elseeeeee")
#                 final_auctions = FinalAuctions.objects.filter(chit=chits, foreman__isnull=False) \
#                     .values('chit', 'bid_amount', 'receiving_member_amount', 'auctiondate', 'default_bid_amount',
#                             'default_chit_amount')
#                 print ("##################################################################################################",final_auctions)
#                 expected_values = FinalAuctions.objects.filter(chit=chits)
#             for i in expected_values:
#                 expected_data = {}
#                 temp = "value0"
#                 serializer = FinalAuctionsViewSerializer(i)
#                 fullexpectedserializer = serializer.data
#                 fullexpectedserializer.update(
#                     {'receiving_member_amount': int(i.default_chit_amount) - int(i.default_bid_amount)})
#                 expected_data[temp] = fullexpectedserializer['receiving_member_amount']
#                 expected_data['chit'] = fullexpectedserializer['chit']
#                 print (fullexpectedserializer['auctiondate'])
#                 expected_data['finaldate'] = fullexpectedserializer['auctiondate']
#                 expected_data['date'] = expected_data['finaldate'][0:10]
#
#                 final_data.append(expected_data)
#             if final_auctions:
#
#                  print("hiiiiiiiiiiii")
#                  prev_data = final_auctions[0]
#                  dict_data = {}
#                  temp = "value1"
#                  for final in final_auctions:
#                      if final['chit'] not in prev_data.values():
#                          count += 2
#                          temp = "value" + str(count)
#                      dict_data['finaldate'] = final['auctiondate']
#                      dict_data['date'] = str(dict_data['finaldate'])[0:10]
#                      print("!!!!!!!!!!!!!!!!!!!!!!!",dict_data['date'])
#                      dict_data['chit'] = final['chit']
#                      dict_data[temp] = final['receiving_member_amount']
#
#
#             a=FinalAuctions.objects.filter(chit=expected_data['chit'],bid_amount__isnull=False).values_list('receiving_member_amount',flat=True)
#             prizemoney=list(map(lambda x:int(x),a))[::-1]
#             print (prizemoney)
#             print("fiiiiiiiiiiiiii",expected_data['chit'],a)
#             sorted_data = sorted(final_data,key=itemgetter('date'))
#             return Response({"chit_data":sorted_data , "prizemoney":prizemoney ,"chit_count": count}, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             print (e)
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

class GetFundDetails(APIView):
    def get(self,request):
        try:
            userid = authentication(request.META['HTTP_AUTHORIZATION'])
            print("userrrrrrrrrrrrrrr",userid)
            member = MemberProfile.objects.get(user = userid)
            data = MemberLoanDetails.objects.filter(status='Disbursed',member_id=member).values('loan_type','paid_amount',
                                                                                                'auction_count','member_count','payment_status','balance','chit',
                                                                                                'member_name','interest_amount','disbursed_date','transaction_id')
            for i in data:
                print("rrrrrrrrrrrr",i)
                chit = Chits.objects.filter(id = i['chit']).values('chit_amount','chit_number','chit_type')
                i['chitdetails'] = chit
            print("55555555555555555",data)
            return Response(data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)




class ProfilePicUpdate(APIView):
    def post(self,request):
        print("jjjjjjjjjjj",request.data)
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        print("555555555555",userid)
        data = MemberProfile.objects.get(user= userid)
        if data:
            data.front_photo = request.data['pic']
            data.save()
            print("successfully profilepic updated")
            return Response("successfully Updated")

class GetClosedFunds(APIView):
    def post(self,request):
        print("rqqqqqqqqqqqqqqqqqqqqqqqqq",request.data)
        data = request.data['chit_id']
        print("chittttttttttttt",data)
        print("myyyyyyyyyyyyyyyyyy",data)
        try:
            print("llllllllllllllllllltry")
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            print("userrrrrrrrrrrrrrrrrrrrr",user)
            member = MemberProfile.objects.get(user = user)
            print("memberrrrrrrrrrrrrrrrrrrrrr",member)
            runningfunds = RunningChits.objects.filter(member = member,chit = data)
            if runningfunds:
                           print("inside ifffffffffffffff")
                           data = FinalAuctions.objects.filter(chit=data).values()
                           for i in data:
                            data1 = Request.objects.filter(member_id=i['member']).values()
                            i['member_name']=data1[0]['member_name']
                            print("dataaaaaaaaaaaaaaaaaaaaa",data)
            return Response(data)

        except Exception as e:
            print(e)

class ProfilePic(APIView):
    def get(self,request):
        print("%%%%%%%%%%%%%%%%%", request.data,len(request.data))
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            prof = MemberProfile.objects.filter(user = user)
            finalval = {}
            dictval = {}
            if prof:
                pic = MemberProfile.objects.filter(user_id = user)
                pic1 = pic.values()
                finalpic = pic[0].front_photo.url
                chitdetails = Request.objects.filter(member_id = pic[0].id).values_list('chit_id',flat = True)
                setval = set(chitdetails)
                listval = list(setval)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", listval[0])
                dictval['chit_id'] = listval[0];
                print("777777777777777777777777", chitdetails)
                cht = Chits.objects.filter(id =  dictval['chit_id']).values('status')
                print("chhhh",cht)

                if chitdetails and finalpic:
                    finalval['finalpic'] = finalpic
                    finalval['chitdetails'] = "showgraph "
                    finalval['chtup'] = cht
                return Response(finalval)
            else:
                pic = ForemanProfile.objects.filter(user = user)
                pic1 = pic.values()
                finalpic = pic[0].front_photo.url
                return Response(finalpic)
        except Exception as e:
            print(e)
            return Response(e)

class Uploadcibilfile(APIView):
    def post(self, request):
            print ("tttt",request.data)
            id = request.data['idff']
            print ("idddd", id)
            datas=MemberProfile.objects.get(id=request.data['idff'])
            datas.cibil_score_file = request.data['membercibil']
            datas.save()
            prof = MemberProfile.objects.filter(id = request.data['idff'])
            data={
                "cibil_file":prof[0].cibil_score_file.url
            }
            print("Image",data)
            return Response(data)


class GetCibiFfile(APIView):
    def post(self,request):
        print("&&&&&&",request.data)
        prof=MemberProfile.objects.filter(mobile_number=request.data['mobile_number'])
        data={
            "image":prof[0].cibil_score_file.url,
                }
        print("image",data)
        return  Response(data)


class Profiledata(APIView):
    def get(self,request):
        print("&&&&&&",request.data)
        id1=authentication(request.META['HTTP_AUTHORIZATION'])
        print('@@@@@@@@@ i am',id1)
        prof=MemberProfile.objects.filter(user_id=id1)

        data={
            "profile_photo":prof[0].front_photo.url,
                }
        print("image",data)
        return  Response(data)

class Memberdocsupload(APIView):
    def post(self,request):
        print ("imageeeeeeeee", request.data)
        try:
            data = MemberProfile.objects.get(id=request.data['id'])
            name = request.data['name']
            if data:
                if name == "pic1":
                    print("inside if")
                    data.agrementcopy=request.data['pic1']
                elif name == 'pic2':
                    data.rtmagrementcopy=request.data['pic1']
                else:
                    data.addagrementcopy=request.data['pic1']
                data.save()
                return  Response("dataaa")
        except Exception as e:
                print(e)
                return Response(status = status.HTTP_200_OK)

class Getmembdoc(APIView):
    def get(self,request):
        print("heeyyyyyy",request.data)
        id1=authentication(request.META['HTTP_AUTHORIZATION'])
        print("cominggg",request.data,id1)
        member = MemberProfile.objects.get(user_id=id1)
        print("zzzzzzz",member)
        data={
            "pic1":member.agrementcopy.url,
            "pic2": member.rtmagrementcopy.url,
            "pic3": member.addagrementcopy.url
                }
        print("pic1",data)
        return Response(data)

class GetTransData(APIView):
    def post(self,request):
        print("WHAT ALL DATA I'M GETTINGGGGGGGGGGG",request.data)
        try:
            id1=authentication(request.META['HTTP_AUTHORIZATION'])
            Alldata = FinalAuctions.objects.filter( chit = request.data['chit'],  member = request.data['member'],
                                           flag = True).values()
            print("ALLLLLLDATAAAAAAAAAAAAA",Alldata)
            chitname = Chits.objects.filter(id = request.data['chit']).values('company_name')
            print("CHITNAMEEEEEEEEEEEEEEEEEEEEE",chitname)

            if Alldata:
                for i in Alldata:
                    i["fundname"] = chitname[0]['company_name']
                    data = MemberLoanDetails.objects.filter( chit = request.data['chit'], member_id = request.data['member']).values()
                    print("RTTTTTTTTTMMMMMMMMMMMMMMM",data)

                    if data:
                        i['penalty_amount'] = data
                        return Response(Alldata)
                    else:
                        return Response(Alldata)
            else:
                return Response("No Data Found")
            return Response(Alldata)
        except Exception as e:
            print(e)
            return Response("FAILED")


class HelpMesForNewMem(APIView):
    def get(self,request):
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%",id)
        data = MemberProfile.objects.filter(user_id = id, is_active = False)
        if  data:
            return Response("successss");
        else:
            print("&&&&&&&&&&&&&&&&&&&")
            return Response("failed");

class StatusForMemGraph(APIView):
    def get(self,request):
        try:
            id = authentication(request.META['HTTP_AUTHORIZATION'])
            grap = Chits.objects.filter(status = 'RUNNING').values()
            if grap:
                res = 'graph'
            else:
                res = 'no graph'
            data = {'msg':res}
            return Response(data)

        except Exception as e:
            print(e)
            data = {'msg': 'failed'}
            return Response(data)