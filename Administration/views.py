# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AdminSerializer,ForemanUpdateSerializer, EditAppMembers
from Members.functions import authentication

from Members.models import MemberProfile
from .models import ExecutiveProfile, RolePermissionFeature
from Foreman.models import Chits, ForemanProfile
from rest_framework import status
from Members.models import MemberProfile


# Create your views here.
class AdminUpcomingFunds(APIView):
    def get(self,request):
        print("oooooooooooooooooooo",request.data)
        user = authentication(request.META['HTTP_AUTHORIZATION'])
        print("userrrrrrr",user)
        upfunds = Chits.objects.filter(check = False, status = 'UPCOMING').count()
        id = ExecutiveProfile.objects.get(user_id=user)

        chits = Chits.objects.filter().values('foreman', 'id','chit_number', 'chit_type', 'chit_amount', 'chit_duration',
                                             'max_bid_amount', 'min_bid_amount', 'chit_location', 'foreman_commission',
                                             'company_name', 'company_logo', 'prize_money', 'amount_in_string',
                                             'duration_in_string','foreman__full_name','foreman__mobile_number','check').order_by('-id')

        data = { "chits":chits, "count":upfunds}
        return Response(data)


class ApproveUcomingFunds(APIView):
    def post(self,request):
        print("qqqqqqqqqq",request.data)
        fundstatus = request.data['status']
        print("llllllllll",fundstatus)
        id = request.data['id']
        if fundstatus == 'APPROVE':
            profile = list(MemberProfile.objects.all().values_list('user',flat=True))
            Chits.objects.filter(id=id).update(check=True)
            data = Chits.objects.filter().values('foreman', 'chit_number', 'chit_type', 'chit_amount', 'chit_duration',
                                                 'max_bid_amount', 'min_bid_amount', 'chit_location',
                                                 'foreman_commission',
                                                 'company_name', 'company_logo', 'prize_money', 'amount_in_string',
                                                 'duration_in_string', 'status', 'chit_score', 'check',
                                                 'foreman__mobile_number', 'foreman__full_name', 'id').order_by('-id')
            finaldata = {"res":"Request Approved","data":data}

        if fundstatus == 'DECLINE':
            Chits.objects.filter(id=id).update(check=False)
            data = Chits.objects.filter().values('foreman', 'chit_number', 'chit_type', 'chit_amount', 'chit_duration',
                                                 'max_bid_amount', 'min_bid_amount', 'chit_location',
                                                 'foreman_commission',
                                                 'company_name', 'company_logo', 'prize_money', 'amount_in_string',
                                                 'duration_in_string', 'status', 'chit_score', 'check',
                                                 'foreman__mobile_number', 'foreman__full_name', 'id').order_by('-id')
            finaldata = {"res": "Request Declined", "data": data}
        return Response(finaldata)

class manage_funds(APIView):
    def get(self,request):
        print("eeeeeeee")
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        profile =ExecutiveProfile.objects.get(user=id)
        print("proffffffff",profile)
        profilerole = profile.role
        print(profilerole)
        if profilerole == 'ADMIN':
            role = Chits.objects.filter().values()
            print('role data.............',role)
            rolecount = role.count()
            print(rolecount)
        data = {"data":role}
        return Response(data)

class UpdateManageFunds(APIView):
    def post(self,request):
        status1 = request.data['status']
        try:
            id = authentication(request.META['HTTP_AUTHORIZATION'])
            profile =ExecutiveProfile.objects.get(user=id)
            print("prooooo",profile)
            if profile:
                print("inssssssssss")
                if status1 == 'Delete':
                    Chits.objects.filter(id=request.data['id']).delete()
                    return Response("chit removed")
                chits=Chits.objects.get(id = request.data['data'][0]['id'])
                adminser = AdminSerializer(chits,request.data['data'][0],partial=True)
                if adminser.is_valid():
                    adminser.save()
                    return Response("serial saved")
            else:
                return Response("he is not an admin")

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class memberlist1(APIView):
    def get(self,request):
        id1 = authentication(request.META['HTTP_AUTHORIZATION'])
        print (id1)
        approved=MemberProfile.objects.filter(is_active=True).values('mobile_number','email_id','full_name','member_rating').order_by('user')
        newmember = MemberProfile.objects.filter(is_active=False).values('mobile_number','email_id','full_name','member_rating').order_by('user')
        unapproved=MemberProfile.objects.filter(is_active=False).values('mobile_number','email_id','full_name','member_rating').order_by('user')
        data={"approved":approved,"newmember":newmember,"unapproved":unapproved,"approved_count":approved.count(),"newmember_count":newmember.count(),"unapproved_count":unapproved.count()}
        return Response(data)



class Approvemember(APIView):
    def post(self,request):
        user = authentication(request.META['HTTP_AUTHORIZATION'])
        if str(request.data['status'])=="decline":
            print("hiiiiiiiiiiiiiiiiiii")
            MemberProfile.objects.filter(mobile_number=request.data['mobile_number']).update(is_active=False)
        elif str(request.data['status'])=="approve":
            MemberProfile.objects.filter(mobile_number=request.data['mobile_number']).update(is_active=True)
            print("hello")
        return Response("success")




class ManageForemanFunds(APIView):
    def get(self,request):
        try:
            userid = authentication(request.META['HTTP_AUTHORIZATION'])
            print(userid)
            data=ExecutiveProfile.objects.get(user = userid)
            print(data)
            if data:
                profile=ForemanProfile.objects.all().values()
                print (profile)
                data = {"data":profile}
                return Response(data)
        except Exception as e:
            print (e)


class UpdateManageForeman(APIView):
    def post(self,request):
        status1 = request.data['status']
        print("fffffffffffffffffffffff",request.data['data']['id'])
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            print("kkkkkkkkkkkkkkk",user)
            profile = ExecutiveProfile.objects.get(user=user)
            if profile:
                if status1 == 'DELETE':
                    ForemanProfile.objects.filter(id = request.data['data']['id']).update(is_active = False)
                    return Response("foreman deleted")
                foreman = ForemanProfile.objects.get(id = request.data['data']['id'])
                print("jnfjgnnnnnnnnnnnnnnnnnnnnnnn", foreman)
                data = ForemanUpdateSerializer(foreman,request.data['data'])
                if data.is_valid():
                    data.save()
                    return Response("data updated successfully")
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ApproveForeman(APIView):
    def post(self,request):
        print("hhhhhhhhhhh",request.data)
        try:
            id1 = authentication(request.META['HTTP_AUTHORIZATION'])
            status1 = request.data['status']
            id2 = request.data['id']
            if status1 == 'APPROVE':
                ForemanProfile.objects.filter(id = id2).update(transaction_verify = True)
                foreman = ForemanProfile.objects.filter(id = id2)
                print("jjjjjjjjjjj",foreman)
                data = foreman[0].transaction_verify
                print("llllllllllll",data)
                data1 = {"PERMISION":data}
                return Response(data1)

            if status1 == 'DECLINE':
                ForemanProfile.objects.filter(id = id2).update(transaction_verify = False , transaction_id = None)
                foreman = ForemanProfile.objects.filter(id = id2)
                data = foreman[0].transaction_verify
                data1 = {"PERMISION": data}
                return Response(data1)

        except Exception as e:
            print(e)




class Memberdetail(APIView):
    def post(self,request):
        print (request.data)
        details=MemberProfile.objects.filter(mobile_number=request.data['mobile_number']).values()
        return Response(details)


class EditApproveMem(APIView):
    def post(self, request):
        print (request.data)
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            if user:
                print("inside userrrrrrr")
                member = MemberProfile.objects.get(mobile_number=request.data['mobile_number'])
                print("meeeeeeeee",member)
                data = EditAppMembers(member,request.data)
                print("fiiiiiiiiiiiiiiiii",data)
                if data.is_valid(Exception):
                    data.save()
                return Response("succ")
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HomeUpcomingfunds(APIView):
    def get(self,request):
        a=[]
        funds=Chits.objects.filter()
        for i, fund in enumerate(funds.values()):
            # print (i,list(enumerate(funds.values())))
            fund['company_logo']=funds[i].company_logo.url
            a.append(fund)
        print (a)
        return Response(a)

class HomeRunningfunds(APIView):
    def get(self,request):
        a=[]
        funds=Chits.objects.filter()
        for i, fund in enumerate(funds.values()):
            # print (i,list(enumerate(funds.values())))
            fund['company_logo']=funds[i].company_logo.url
            a.append(fund)
        print (a)
        return Response(a)



class Chit_Details(APIView):
    def post(self,request):
        total = ''
        print (request.data)
        try:
            company = request.data[0]
            location = request.data[1]
            duration = request.data[2]
            amount = request.data[3]
            chit_status = request.data[4]
            print (chit_status)
            if chit_status == 'UPCOMING':

                if company:
                    comp = list(Chits.objects.filter(company_name__in=company).values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))
                else:
                    comp = list(Chits.objects.filter().values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))

                if location:
                    loc = list(Chits.objects.filter(chit_location__in=location, id__in=comp).values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))
                else:
                    loc = list(Chits.objects.filter().values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))

                if duration:
                    dur = list(Chits.objects.filter(duration_in_string__in=duration, id__in=loc).values_list(flat=True).exclude(Q(status='RUNNING')| Q(status='CLOSED')))
                else:
                    dur = list(Chits.objects.filter().values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))

                if amount:
                    amn = list(Chits.objects.filter(amount_in_string__in=amount, id__in=dur).values_list(flat=True).exclude(Q(status='RUNNING')| Q(status='CLOSED')))
                else:
                    amn = list(Chits.objects.filter().values_list(flat=True).exclude(Q(status='RUNNING')|Q(status='CLOSED')))

                if not company and not location and not duration and not amount:
                    data4 = list(set().union(comp, loc, dur, amn))
                    data4 = data4[::-1]
                else:
                    data4 = list(set(set(set(set(comp).intersection(loc)).intersection(dur)).intersection(amn)))
                totalcount = len(data4)
                data = data4
                result = []
                for out in data:
                    chit = Chits.objects.filter(id=out).exclude(Q(status='RUNNING')| Q(status='CLOSED'))
                    for chits in chit:

                        rating = '5'

                        data1 = {"company_name": chits.company_name,
                                 "chit_duration": chits.chit_duration,
                                 "chit_amount": chits.chit_amount,
                                 "company_logo": chits.company_logo.url,
                                 "chit_location": chits.chit_location,
                                 "max_bid_amount": chits.max_bid_amount,
                                 "min_bid_amount": chits.min_bid_amount,
                                 "foreman_commission": chits.foreman_commission,
                                 "chit_type": chits.chit_type,
                                 "chit_number": chits.chit_number,
                                 "rating": rating}
                        result.append(data1)
                total = {"VALUES": result, "COUNT": totalcount,"STATUS": chit_status}
            else:
                if company:
                    comp = list(Chits.objects.filter(company_name__in=company).values_list(flat=True).exclude(
                        Q(status='UPCOMING') | Q(status='CLOSED')))
                else:
                    comp = list(
                        Chits.objects.filter().values_list(flat=True).exclude(Q(status='UPCOMING') | Q(status='CLOSED')))

                if location:
                    loc = list(Chits.objects.filter(chit_location__in=location, id__in=comp).values_list(flat=True).exclude(
                        Q(status='UPCOMING') | Q(status='CLOSED')))
                else:
                    loc = list(
                        Chits.objects.filter().values_list(flat=True).exclude(Q(status='UPCOMING') | Q(status='CLOSED')))

                if duration:
                    dur = list(
                        Chits.objects.filter(duration_in_string__in=duration, id__in=loc).values_list(flat=True).exclude(
                            Q(status='UPCOMING') | Q(status='CLOSED')))
                else:
                    dur = list(
                        Chits.objects.filter().values_list(flat=True).exclude(Q(status='UPCOMING') | Q(status='CLOSED')))

                if amount:
                    amn = list(Chits.objects.filter(amount_in_string__in=amount, id__in=dur).values_list(flat=True).exclude(
                        Q(status='UPCOMING') | Q(status='CLOSED')))
                else:
                    amn = list(
                        Chits.objects.filter().values_list(flat=True).exclude(Q(status='UPCOMING') | Q(status='CLOSED')))

                if not company and not location and not duration and not amount:
                    data4 = list(set().union(comp, loc, dur, amn))
                    data4 = data4[::-1]
                else:
                    data4 = list(set(set(set(set(comp).intersection(loc)).intersection(dur)).intersection(amn)))
                totalcount = len(data4)
                data = data4
                result = []
                for out in data:
                    chit = Chits.objects.filter(id=out).exclude(Q(status='UPCOMING') | Q(status='CLOSED'))
                    for chits in chit:
                        rating = '5'

                        data1 = {"company_name": chits.company_name,
                                 "chit_duration": chits.chit_duration,
                                 "chit_amount": chits.chit_amount,
                                 "company_logo": chits.company_logo.url,
                                 "chit_location": chits.chit_location,
                                 "max_bid_amount": chits.max_bid_amount,
                                 "min_bid_amount": chits.min_bid_amount,
                                 "foreman_commission": chits.foreman_commission,
                                 "chit_type": chits.chit_type,
                                 "chit_number": chits.chit_number,
                                 "rating": rating}
                        result.append(data1)
                total = {"VALUES": result, "COUNT": totalcount,"STATUS": chit_status}
        except Exception as e:
            print (e)
        return Response(total, status=200)

class AdminRunChits(APIView):
    def post(self,request):
        print("ooooooooooo",request.data)
        foreman = ForemanProfile.objects.get(id=request.data['id'])
        print("ssssssssssssssssssss", foreman)
        running_chits = Chits.objects.filter(foreman_id=foreman, status='RUNNING')
        running_dict = running_chits.values()
        print("hhhhhhhhhhh", running_dict)
        for i, running in enumerate(running_dict):
            running['company_logo'] = running_chits[i].company_logo.url
        return Response(running_dict, status=status.HTTP_200_OK)


class GetExecutiveinfo(APIView):
    def get(self,request):
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            executiveinfo = ExecutiveProfile.objects.filter().values()
            return Response(executiveinfo)
        except Exception as e:
            print("eroo111111111111111111000rrr", e)
            return Response("failed")