# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Max
from django.shortcuts import render
import json


from Members.models import Request, MemberProfile,Transactions
from Rtm.models import MemberLoanDetails
from .models import ForemanProfile,Chits, RunningChits,FinalAuctions,Auctions
# from .models import ForemanProfile,Chits
from rest_framework.response import Response
import datetime
from django.contrib.auth.models import User
from rest_framework import status
from django.db import transaction
from Members.functions import encrypt_password
import logging
import traceback
from rest_framework.views import APIView
from Members.functions import authentication
from .serializers import ForemanSerializer, EditForeman
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from dateutil import parser as date_parser
from Members.functions import authUserId



logger = logging.getLogger(__name__)
# Create your views here.
def get_foreman_id():
    count = ForemanProfile.objects.all().count()
    if count != 0:
        customid = "F" + str(count + 1)
    else:
        customid = "F1"
    return customid



class ForemanRegistration(APIView):
    def post(self,request):
        print("yyyyyyyyy",request.data)
        full_name = request.data['fullname']
        print("&&&&&&&&&&", full_name)
        # date_of_birth = request.data['date_of_birth']
        dateofbirth = request.data['date'][4:24]
        print("RRRRRRRR",dateofbirth )
        date_of_birth = datetime.datetime.strptime(dateofbirth, "%b %d %Y %H:%M:%S").date()
        # print("AAAAAA",date_of_birth)
        finaldate = datetime.datetime.strftime(date_of_birth, '%Y-%m-%d')
        mobile_number = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=mobile_number, is_active=True)
            if user:
                return Response("User already exists", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            try:
                print("inside try block")
                with transaction.atomic():
                    user = User()
                    encrypt = encrypt_password(password)
                    user.username = mobile_number
                    user.password = encrypt
                    user.last_name = ""
                    user.first_name = full_name
                    user.is_active = True
                    user.id=authUserId()
                    user.save()
                    userid = User.objects.get(id=user.id)
                    print("uuuuuuuuseeeeeeeeeeeeeeeerrrrrrrrrrrid",userid)
                    profile = ForemanProfile()
                    profile.user = userid
                    profile.full_name = full_name
                    profile.date_of_birth = finaldate
                    print("Date of birth Is SSSSS",profile.date_of_birth)
                    profile.mobile_number = mobile_number
                    profile.id = get_foreman_id()
                    profile.is_active = True
                    profile.save()
                    time = datetime.datetime.now()
                    logger.info("######################################################")
                    logger.info("New Member registered " + full_name + " " + str(mobile_number) + " " + profile.id +
                                " @ " + str(time))
                    logger.info("######################################################")
                return Response("Registration success", status=status.HTTP_200_OK)
            except Exception as e:
                tb = traceback.format_exc()
                print(e)
                logger.info("######################################################")
                logger.info("Profile Update " + str(id) + " " + " Failed")
                logger.info("######################################################")
                return Response("Registration failed", status=status.HTTP_400_BAD_REQUEST)



class NewChit(APIView):
    def post(self,request):
        try:
            print("4444444444444444",request.data)
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            foreman = ForemanProfile.objects.get(user=user)
            print("fffffffff",foreman)
            data = request.data['chit']
            print("99999999999999999",data)
            chits = Chits()
            chits.company_name =  foreman.chit_company
            chits.company_logo = foreman.chit_company_logo
            chits.amount_in_string = amount_in(data['chitamount'])
            chits.duration_in_string = duration_in(data['chitduration'])
            chits.chit_duration = data['chitduration']
            chits.chit_location = data['chitlocation']
            chits.chit_amount = data['chitamount']
            chits.chit_duration = data['chitduration']
            chits.max_bid_amount = data['max_bid_amount']
            chits.min_bid_amount = data['min_bid_amount']
            chits.foreman_commission = data['foreman_commission']
            chits.chit_number = get_chit_number(foreman.id)
            chits.foreman_id = foreman
            chits.chit_type = request.data['type']
            startdate = datetime.datetime.today()
            chits.startdate = str(startdate)[:10]
            chits.save()
            return Response("Chit Saved Successfully",status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("contact customer service")


def amount_in(amount):
    print("inside amount ")
    if int(amount) in range(1, 100001):
        a = 'i'
    elif int(amount) in range(100001, 500001):
        a = 'j'
    elif int(amount) in range(500001, 1000001):
        a = 'k'
    elif int(amount) in range(1000001, 5000001):
        a = 'l'
    elif int(amount) in range(5000001, 10000001):
        a = 'm'
    else:
        a = "enter amount number correctly"
    return str(a)

def duration_in(duration):
    print("inside duration",duration)
    if int(duration) in range(1, 21):
        x = 'a'
    elif int(duration) in range(21, 31):
        x = 'b'
    elif int(duration) in range(31, 41):
        x = 'c'
    elif int(duration) in range(41, 51):
        x = 'd'
    elif int(duration) in range(51, 101):
        x = 'e'
    else:
        x = "enter amount number correctly"
    return x


def get_chit_number(foreman_id):
    print("inside   set chitttttt")
    foreman = ForemanProfile.objects.get(id=foreman_id)
    print("tttttttt",foreman)
    count = Chits.objects.filter(foreman=foreman_id)
    print("couuuuuuuuu",count)
    data = count.count()
    print("datataaaaaaa",data)
    if count != 0:
        data1 = foreman.chit_company
        print ("dddddddddddddd",foreman.chit_company)
        customid = data1 + '-' + str(data + 1)
        print("c111111111",customid)
    else:
        customid = foreman.chit_company + '-' " 1"
        print("cc333333",customid)
    return customid


class ForemanFinalRegister(APIView):
    def post(self,request):
        print("requestttttttttt",request.data)
        x = json.loads(request.data['data1'])
        y = json.loads(request.data['data2'])
        x.update(y)
        print("cccccccccc", request.data['front_photo'])

        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            foreman = ForemanProfile.objects.get(user=user)
            # x['ifsc_code'] = x['a']+x['ifsc_code']
            # x['bank_name'] = x['bank1'] 0
            print("inside tryyyyyyyyyyyyyyyyyyyyyyy",foreman)
            obj = ForemanSerializer(foreman,x)
            print("serializationnnnnnnnnnnnnnnnnnnnnnn",obj)

            if obj.is_valid(raise_exception=True):
                obj.save()
                print("serialnnnnnnnn after saveeeeeeeeee", obj)

                if request.data['front_photo']:
                    foreman.front_photo = request.data['front_photo']
                    foreman.save()
                    print("profileee piccccccccccc after saveeeeeeeeee", obj)

            return Response('success')
        except Exception as e:
            print (e)
        return Response("failed")



class ForemanUpload(APIView):
    def post(self,request):
        try:
            userid = authentication(request.META['HTTP_AUTHORIZATION'])
            data1 = ForemanProfile.objects.filter(user=userid)
            data2 = Chits.objects.filter(foreman=data1[0].id)

            if data1 or data2:
                for key in request.data:
                    if key == 'val':
                        data1[0].certificate_of_registration = request.data['val']
                        data1[0].save()
                    elif key == 'address':
                        data1[0].address_proof = request.data['address']
                        data1[0].save()
                    elif key == 'fretarnity':
                        data1[0].chit_company_logo = request.data['fretarnity']
                        data1[0].save()
                        for i in range(len(data2)):
                            data2[i].company_logo = request.data['fretarnity']
                            data2[i].save()
                    else:
                        data1[0].bank_statement = request.data['bankstate']
                        data1[0].save()
            return Response("uploaded successfully")
        except Exception as e:
            print(e)
            return Response("failed")



class ForemanViewProfile(APIView):
    def get(self,request):
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            print(user)
            data1 = ForemanProfile.objects.get(user = user)
            print(data1)
            if data1:
                data = ForemanProfile.objects.filter(id=data1).values()
                print(data)
                return Response(data)
        except Exception as e:
            print(e)

class EditForemanProfile(APIView):
    def post(self,request):
        try:
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            data1 = ForemanProfile.objects.get(user = user)
            data = EditForeman(data1,request.data[0])
            if data.is_valid(Exception):
                data.save()
                return Response("succesfully updated")
        except Exception as e:
            print (e)



class Foreman_Requested_Chits(APIView):
    def get(self,request):
        try:
            print("llllllllllllllll")
            profile = authentication(request.META['HTTP_AUTHORIZATION'])
            foreman = ForemanProfile.objects.get(user=profile)
            requests = list(Request.objects.filter(foreman_id=foreman).values_list('chit_id', flat=True))
            chits = Chits.objects.filter(check=True,foreman=foreman, status='UPCOMING').order_by('-id')
            chits_dict = chits.values()
            count = Chits.objects.filter(check=True, status='UPCOMING').count()
            for idx, chit_dict in enumerate(chits_dict):
                chit_dict['company_logo'] = chits[idx].company_logo.url
            return Response({"count": count, "chit_dict": chits_dict})
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)




class Forman_Reuqest(APIView):
    def post(self,request):
        print("kkkkkkkkkkkkk",request.data)
        profile = authentication(request.META['HTTP_AUTHORIZATION'])
        fore1 = ForemanProfile.objects.get(user=profile)
        chit = request.data['chit']
        chit_requests = Request.objects.filter(chit_id=chit,foreman_id=fore1,add_check=False,added_members=True).exclude(check=False)
        if chit_requests:
            data = chit_requests.values()
            memdata = data[0]['member_number']
            for i in data:
                membercibil = MemberProfile.objects.filter(id=i['member_id'])
                if membercibil :
                    i['cibilForemanHome_score'] = membercibil[0].cibil_score
                    i['cibil_score_file'] = membercibil[0].cibil_score_file.url
                    i['rating'] = membercibil[0].member_rating
            result = {"data": data, "chitid": chit,"memberData" : membercibil.values()}
            print("finallllllllllllllllll", result)
            return Response(result)
        else:
            return Response("As per chit limit is crossed")

class UpdateForemanScore(APIView):
    def post(self,request):
        try:
            id = authentication(request.META['HTTP_AUTHORIZATION'])
            profile = ForemanProfile.objects.get(user=id)
            # print("insideeeeeee **************************************",i)
            # profile = ForemanProfile.objects.get(mobile_number = memdata)
            print("memberrrrrrrrrrrrrrrrrrrrrrrrrr",profile)

            member_date_of_birth = profile.date_of_birth
            print("DTAEEEEEEEEEEEEEEEEEEEEE",member_date_of_birth)
            current_date = datetime.datetime.now()
            print("evaginnnnnnnnnntimeeeeeeeeeeeee",current_date)
            age = current_date.year - member_date_of_birth.year
            print("givemeeeeeeeeeeeeeeeeeeeeeeee",age)
            profile.gchits_score = 0
            if profile.gender == 'Male':
                profile.gchits_score += 10
            if profile.gender == 'Female':
                profile.gchits_score += 10
            if profile.aadhaar_card:
                profile.gchits_score += 20
            if profile.applicant_pancard_number:
                profile.gchits_score += 20
            if profile.company_pancard_number:
                profile.gchits_score += 10
            if profile.marital_status == 'Unmarried' :
                profile.gchits_score += 10
            elif profile.marital_status == 'Married':
                profile.gchits_score += 30
            if profile.employment_type:
                profile.gchits_score += 10
            if profile.business_bank_statement:
                profile.gchits_score += 20
            
            if profile.present_address_type == 'Owned':
                profile.gchits_score += 50
            if profile.present_address_type == 'Rented':
                profile.gchits_score += 10
            if profile.organization_type:
                profile.gchits_score += 50
            if profile.designation:
                profile.gchits_score += 20

            if profile.bank_statement:
                profile.gchits_score += 50
            if profile.company_pancard:
                profile.gchits_score += 70

            if profile.address_proof:
                profile.gchits_score += 60
            if profile.annual_salary:
                profile.gchits_score += 10
            if profile.employee_id_card:
                profile.gchits_score += 70

            if profile.certificate_of_registration:
                profile.gchits_score += 50

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
            if profile.company_address_proof:
                profile.gchits_score += 50
            if profile.aggrement :
                profile.gchits_score += 20
            profile.save()
            print("555555555554444444444444",profile.gchits_score)

            return Response(profile.gchits_score)
        except Exception as e:
            print("555555555554444444444444",e)
            return Response("failed")


class Members_Add(APIView) :
    def post(self,request):
        status1 = request.data['status']
        member = request.data['member_id']
        chit = request.data['chit_id']
        foreman = request.data['foreman_id']
        id1 = request.data['id']
        # id2 = request.data['id2']
        member_chit_count = request.data['member_chit_count']
        profile = MemberProfile.objects.filter(id=member)
        fore1 = ForemanProfile.objects.filter(id=foreman)
        details = Chits.objects.filter(id=chit)
        if status1 == "ADD":
            count = details[0].chit_duration
            # running = RunningChits.objects.filter(member=member, foreman=foreman, chit=chit, is_active=True)
            count1 = RunningChits.objects.filter(chit=chit, is_active=True)
            print("testttt",profile[0].credit_limit)
            if profile[0].credit_limit < details[0].chit_amount:
                data = "Member credit limit is very low, Contact member or view member credit details. "
            elif count == count1.count():
                data = "As per your chit members limit crossed"
            else:
                a=RunningChits.objects.filter(member=member,member_count=member_chit_count).values()
                credit = profile[0].credit_limit-details[0].chit_amount
                profile[0].credit_limit = credit
                if not (RunningChits.objects.filter(foreman = foreman,member=member,chit=chit, member_count=member_chit_count )):
                    chits = RunningChits()
                    chits.foreman = foreman
                    chits.member = member
                    chits.chit = chit
                    chits.member_count = member_chit_count
                    chits.save()
                MemberProfile.objects.filter(id=member).update(credit_limit=credit)
                Request.objects.filter(id=id1,).update(add_check=True,check=False)
                memlist = []
                memberlist = []
                run = RunningChits.objects.filter(chit=chit, is_active=True).count()
                if run == count:
                    run1 = list(RunningChits.objects.filter(chit=chit, is_active=True,added_member_status=True).values_list('member', flat=True))
                    for i in run1:
                        j = str(i)
                        member1 = MemberProfile.objects.filter(id=j)
                        token = str(member1[0].device_token)
                        memlist.append(token)
                        memberlist.append(member1[0].id)
                else:
                    member1 = MemberProfile.objects.filter(id=member)
                    token = str(member1[0].device_token)
                    memlist.append(token)
                    memberlist.append(member)
                mem = check_member(request, details, count1)
                fore = "member added successfully"
                data = {"memberres": mem, "foremanres": fore, "membertoken": memlist,
                        "foremantoken": fore1[0].device_token, "member": memberlist, "chitid": chit}
            return Response(data)
        else:
            RunningChits.objects.filter(id=id1).update(is_active=False)
            Request.objects.filter(id=id1).update(add_check=False, check=True,added_members=False)

            revamount = profile[0].credit_limit
            MemberProfile.objects.filter(id=member).update(credit_limit=revamount)
            chitdetails1 = transaction_status(chit)
            data = {"message": "chit request rejected by particular foreman", "details": chitdetails1}
        return Response(data)




def transaction_status(chitid):
    chitdetails = RunningChits.objects.filter(chit=chitid, is_active=True)
    chitdetails1 = []
    for i in chitdetails:
        member1 = MemberProfile.objects.filter(id=i.member)
        name = member1[0].full_name
        number = member1[0].mobile_number
        if i.transcationid == None:
            transcationid = 'No_Transaction_Id'
        else:
            transcationid = i.transcationid
        if i.trans_verify == None:
            transvfy = "novalue"
        else:
            transvfy = i.trans_verify
        memid = Request.objects.filter(chit_id=chitid, member_id=i.member)
        data = {"membername": name, "number": number, "member_id": i.member, "foreman_id": i.foreman,
                "tarnsactionid": transcationid, "id2": i.id, "chitid": i.chit,
                "transverify": transvfy, "id1": memid[0].id}
        chitdetails1.append(data)
    return chitdetails1


def check_member(request, details, count1):
    count = count1.count()
    left = details[0].chit_duration-count
    if details[0].chit_duration == count:
        data = str(details[0].chit_duration) + " " + " members are added to chit plz deposit amount to foreman " \
                                                     "account within 24hrs "
    else:
        data = str(left) + " " + "members left to start chit if they added we inform you to deposit amount " \
                                 "on particular date"
    return data





class Added_members(APIView):
    def post(self,request):
        print("99999999999",request.data)
        try:
            if not request.data['status'] == '':
                print("rrrrrrrrr")
                if request.data['status'] == 'REJECT':
                    print("ooooooooooooooooooooo")
                    RunningChits.objects.filter(chit=request.data['data']['chitid'],member=request.data['data']['member_id'],member_count=request.data['data']['count']).update(added_member_status = False,is_active = False)
                    Request.objects.filter(member_id=request.data['data']['member_id'],chit_id=request.data['data']['chitid'],member_chit_count=request.data['data']['count']).update(add_check=False,check=True)
                    return Response("member rejected")
            else:
                id1 = request.data['chit']
                data = {}
                chit = RunningChits.objects.filter(chit=id1, is_active=True,added_member_status=True).order_by('member')
                print ("ttttttttt",chit)
                memberlist = []
                for i in chit:
                    member = MemberProfile.objects.filter(id=i.member)
                    print("meeeeee",member)
                    name = member[0].full_name
                    number = member[0].mobile_number
                    print("nnnnnnnnnnnnnnnnnnnnnnn",name)
                    if i.transcationid == None:
                        transcationid = 'No Transaction ID'
                    else:
                        transcationid = i.transcationid
                    if i.trans_verify == None:
                        transvfy = "novalue"
                    else:
                        transvfy = i.trans_verify

                    memid = Request.objects.filter(chit_id=id1, member_id=i.member,check=False)
                    counts = memid.values_list('member_chit_count',flat=True)
                    print("couuuuuuuuuu",counts)


                    data = {"membername": name, "number": number, "member_id": i.member, "foreman_id": i.foreman,
                                "tarnsactionid": transcationid, "id2": i.id, "chitid": i.chit, "transverify": transvfy,
                                "id1": memid[0].id,"count":i.member_count}
                    memberlist.append(data)
                    dur = Chits.objects.filter(id=id1)
                    chit = RunningChits.objects.filter(chit=id1, trans_verify=True, is_active=True).count()
                    print("pppppppp",dur[0].id)
                    if chit == dur[0].chit_duration:
                        auction1 = "TRUE"
                    else:
                        auction1 = "FALSE"

                data = {"member": memberlist, "AUCTION": auction1,"chitsid":dur[0].id}
                print ("fronttttttttttttttttt",data)

                return Response(data)
        except Exception as e:
            print ("eroooooooooooor",e)
            return Response(status.HTTP_400_BAD_REQUEST)




class Approve_trans(APIView):
    def post(self,request):
        print (request.data)
        status1 = request.data['status']
        id1 = request.data['id2']
        chit = request.data['chitid']
        chitid = chit
        run = RunningChits.objects.filter(id=id1)
        print (run)
        member = MemberProfile.objects.filter(id=run[0].member)
        token = member[0].device_token
        auction1 = ""
        if status1 == "VERIFIED":
            RunningChits.objects.filter(id=id1).update(trans_verify=True)
            dur = Chits.objects.filter(id=chit)
            chit = RunningChits.objects.filter(chit=chit, trans_verify=True, is_active=True).count()
            if chit == dur[0].chit_duration:
                auction1 = "TRUE"
            chitdetails1 = transaction_status(chitid)
            data = {"res": "your Transactionid is verified", "token": token, "AUCTION": auction1, "details": chitdetails1}
            return Response(data)
        if status1 == "newid":
            print("hiiiiiiiiiii")
            RunningChits.objects.filter(id=id1).update(trans_verify=True, transcationid=request.data['newid'], depdate=datetime.datetime.today())
            data = {"res": "Transaction id is saved", "token": token, "AUCTION": auction1}
            return Response(data)
        else:
            RunningChits.objects.filter(id=id1).update(trans_verify=False, transcationid=None, depdate=None)
            chitdetails1 = transaction_status(chitid)
            data = {"res": "your Transactionid is rejected plz re-enter the transactionid", "token": token,
                    "AUCTION": auction1, "details": chitdetails1}
            return Response(data)

class auctionupdate(APIView):
    def post(self,request):
        print('----------',request.data)
        id = request.data['id']
        date = request.data['date']
        FinalAuctions.objects.filter(chit=id).update(next_date=date)
        return Response('sssss')


class AuctionDate(APIView):
    def post(self,request):

        id = request.data['id']
        # print (date_parser.parse(request.data['event']))
        print ("cxcxcxcx", request.data)
        date1 = datetime.datetime.strptime(request.data['event'],'%a, %d %b %Y %H:%M:%S %Z')
        print ("cxcxcxcx", request.data)
        chit = Chits.objects.filter(id=id)
        Chits.objects.filter(id=id).update(status="RUNNING")
        amount = chit[0].chit_amount / chit[0].chit_duration
        RunningChits.objects.filter(chit=id).update(auctiondate=date1)
        self.assign_members(id)
        return Response('sssss')

    def assign_members(self,id):
        chit = Chits.objects.filter(id=id)
        duration = chit[0].chit_duration
        total_amount = chit[0].chit_amount
        run = RunningChits.objects.filter(chit=id)
        date1 = run[0].auctiondate
        current = int(duration) - 1
        j = 1
        for i in range(1, int(duration) + 1):
            final = FinalAuctions()
            final.auction_count = i
            final.chit = chit[0].id
            final.auctiondate = date1 + relativedelta(months=i - 1)
            final.next_date = date1 + relativedelta(months=i)
            final.default_bid_amount = int((total_amount * 0.15) / 12) * current
            final.default_chit_amount = int(total_amount)
            if final.default_bid_amount < (total_amount * .05):
                print("iffff VALAGAAAAAAAAAAAAAAAAAAAA")
                if final.default_bid_amount == (total_amount * .05):
                    final.default_chit_amount = total_amount
                    # final.default_bid_amount = int(total_amount * .05)
                    final.default_bid_amount = int((total_amount * 0.15) / 12) * current
                else:
                    print("else VALAGAAAAAAAAAAAAAAAAAA")
                    # final.default_chit_amount = (int(total_amount) + int(((total_amount * 0.15) / 12) * j))
                    # final.default_bid_amount = int(total_amount * .05)
                    final.default_chit_amount = total_amount
                    final.default_bid_amount = int((total_amount * 0.15) / 12) * current
                    j += 1
            # final.payable_amount = int(round(
            #     (final.default_chit_amount - (final.default_bid_amount - (int(total_amount * .05)))) / int(duration)))
            final.payable_amount = 4700
            if (i == int(duration)):
                final.payable_amount = 0;
            final.save()
            current = (current) - 1

        return "saved"



class ForemanHome(APIView):
    def get(self,request):
        profile = authentication(request.META['HTTP_AUTHORIZATION'])
        print('---------',profile)
        profile = ForemanProfile.objects.get(user_id=profile)
        chits = Chits.objects.filter(foreman_id=profile, status='RUNNING').values('id','chit_amount','startdate','chit_number',).order_by('-id')
        detail=[]
        if chits:
            dict1 = {}
            dict2 = {}
            dict11 = {}
            for i in chits:
                final = FinalAuctions.objects.filter(chit=i['id']).exclude(member=None, foreman=None, bid_amount=None).values(
                    "auction_count", "receiving_member_amount", "chit")
                if final:
                    print("if final",final)
                    list_deatils = filter(lambda x: len(x) != 0, final)
                    for i in list_deatils:
                        dict1.setdefault(i['chit'], []).append(i['auction_count'])
                    for j in dict1.keys():
                        chit = Chits.objects.filter(id=j)
                        max_count = len(dict1[j])
                        final1 = FinalAuctions.objects.filter(chit=j, auction_count=max_count)
                        dict3 = {}
                        dict3['chit_id'] = chit[0].id
                        dict3['start_date'] = chit[0].startdate
                        if int(chit[0].chit_duration) == max_count:
                            dict3['next_auction_date'] = 'Auction Completed'
                        else:
                            dict3['next_auction_date'] = final1[0].next_date
                        dict3['fund_amount'] = chit[0].chit_amount
                        dict3['chit_name'] = chit[0].chit_number
                        dict3['amount'] = final1[0].receiving_member_amount
                        dict3['auction_count'] = max_count
                        dict3['auction_date'] = final1[0].auctiondate
                        dict3['foreman_transaction'] = final1[0].foreman_transaction
                        dict3['hour_difference'] = final1[0].auctiondate + datetime.timedelta(seconds=3600)
                        dict2[j] = dict3

                else:

                    final1 = FinalAuctions.objects.filter(chit=i['id']).values("auction_count", "receiving_member_amount",
                                                                         "chit","auctiondate")
                    print("elseeeeeeeeeeeeeeeeeabcd",final1[0])
                    list_deatils = filter(lambda x: len(x) != 0, final1)
                    print ("detaiiiiiiiiiiil",list_deatils)
                    for i in list_deatils:
                        dict11.setdefault(i['chit'], []).append(i['auction_count'])
                    nolist = map(str, dict11.keys())
                    nolist1 = map(int, nolist)
                    print ("kkkkkkkkkkkkkkkkkkkkk",dict11.keys())
                    # finallist = set(chits) - set(nolist1)
                    for j in dict11.keys():
                        print ("jjjjjjjjjjjjjjjjj",j)
                        chit = Chits.objects.filter(id=j)
                        dict4 = {}
                        dict4['chit_id'] = chit[0].id
                        dict4['start_date'] = chit[0].startdate
                        dict4['chit_name'] = chit[0].chit_number
                        dict4['amount'] = "0"
                        dict4['auction_count'] = "0"
                        dict4['next_auction_date']=final1[0]['auctiondate']
                        dict4['hour_difference'] = final1[0]['auctiondate'] + datetime.timedelta(seconds=3600)
                        print('Trying something',dict4['hour_difference'],final1[0]['auctiondate'])
                        dict2[j] = dict4
                        print("lllllllllllll")
                        detail.append(dict4)
                        print ("hiiiii")
            return Response(dict2)
        return Response("No Records Found")



class ForemanRunningFunds(APIView):
    def get(self,request):
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        foreman = ForemanProfile.objects.get(user = userid)
        running_chits = Chits.objects.filter(foreman_id =foreman,status='RUNNING')
        running_dict = running_chits.values().order_by('-id')
        print("hhhhhhhhhhh",running_dict)
        for i , running in enumerate(running_dict):
            running['company_logo'] = running_chits[i].company_logo.url
        return Response(running_dict,status=status.HTTP_200_OK)

class MemberAuctiontrans(APIView):
    def post(self,request):
        print("wwwwwwwwwww",request.data)
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        profile = ForemanProfile.objects.get(user = userid)
        status = request.data['chit_id']
        auctiondetails = []
        if status == 'RUNNING':
            print("insideeeee ifffff")
            data = list(Chits.objects.filter(foreman=profile, status=status).values_list('id', 'chit_number',
                                                                                            'company_logo'))
            count1 = len(data)
            if count1 == 0:
                data1 = 'No Data Found'
            else:
                data1 = data
            return Response(data1)
        elif status != 'RUNNING':
            print("inside 2lseeeeeeeee")
            chit = Chits.objects.filter(id=status)
            print("fffffffff",chit)
            duration = chit[0].chit_duration
            auctioncount = []
            for i in range(1, int(duration) + 1):
                trans = Transactions.objects.filter(chit=status, auction=i)
                print("traaaaaaa",trans)
                details = trans.values()
                for i in details:
                    print("%%%%%%%%%%%",i['auction'])
                    auctioncount.append(i['auction'])
                print("funnyyyyyyyy",details,type(details))
                auctiondetails.append(details)
                data3 = filter(lambda x: len(x) != 0, auctiondetails)
                # data3.reverse()
                print("dssssswwwwwwwwwww",data3)
            return Response(data3)


class TransactionAuctionHistory(APIView):
    def post(self,request):
        print("uuuuuuu",request.data)
        # memb= RunningChits.objects.filter(chit=request.data['fund_id']).values_list('member',flat=True)
        # list1 = list(memb)
        chitduration = Chits.objects.filter(id=request.data['fund_id']).values('chit_duration')
        memlist = []
        membdict=[]
        med1=[]
        a=datetime.datetime.now()
        # for i in set(memb):
        trans=Transactions.objects.filter(chit=request.data['fund_id'],auction=request.data['auction']).values('id')
            # running = RunningChits.objects.filter(member=i,chit=request.data['fund_id']).values_list('member_count',flat=True)
            # for x in running:
        print (trans)
        obj = Transactions.objects.filter(chit=request.data['fund_id'],auction=request.data['auction'])
        if obj:
                    # for k in trans:
                    #     print (len(k))
                    #     memlist.append(k['id'])
                    #     for p in memlist:
                    #         # print(memlist[0])
                    #         if p not in med1:
                    #             med1.append(p)
                                member = []
                                for l in trans:
                                    print (l)
                                    data1=Transactions.objects.get(id=l['id'],auction=request.data['auction'])
                                    members = MemberProfile.objects.filter(id=data1.member).values()
                                    data2={"id":data1.member,"transaction_id":data1.transaction_id,"trans_date":data1.trans_date,"paid_amount":data1.paid_amount,"check":data1.check,"auction_count":data1.auction,
                                           "rtm_status":data1.rtm_status,"chit_duration":chitduration[0]['chit_duration'],"member":members,
                                           "chitid":request.data['fund_id'],"auction":request.data['auction'],"member_count":data1.mem_count,"id1":data1.id}
                                    # print("data22222222222222222222222222222",data2)
                                    member.append(data2)
        else:
                    m = MemberProfile.objects.filter(id=i).values()
                    n = Transactions.objects.filter().values()
                    print("nnnnnnnnnnnnnnn11111111111111111111",n)
                    data={"id":i,"transaction_id":None,"rtm_status":n[0]['rtm_status'],"member_name":m[0]['full_name'],"member":m,"chitid":request.data['fund_id'],
                          "auction":request.data['auction'],"chit_duration":chitduration[0]['chit_duration'],"member_count":x}
                    membdict.append(data)
        c=datetime.datetime.now()
        f=c-a
        print (f)
        data3=list(membdict+member)
        # print("dataaaaaaaa333333333333333333333333333",data3)
        return Response(data3)


class Auctiondata(APIView):
    def post(self,request):
        print("pppppppppppppppp",request.data)
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        member = MemberProfile.objects.get(user = id)
        chit = request.data['id']
        foreman=Chits.objects.filter(id=chit).values('foreman_id')
        foreman = foreman[0]['foreman_id']
        print("sssssssssssss", foreman)
        bid_amount = request.data['bid']
        date1 = RunningChits.objects.filter(chit=chit)
        var = FinalAuctions.objects.filter(chit=chit, foreman=foreman, member=member).values('member').count()
        membercount = Transactions.objects.filter(chit=chit,member=member,foreman=foreman).values_list('mem_count',flat=True).distinct()
        verchit = Chits.objects.filter(id=chit)
        amount = verchit[0].chit_amount
        min_amt1 = FinalAuctions.objects.filter(chit=chit,foreman=None, member=None,bid_amount=None).values('default_bid_amount').first()

        max_amt = int(amount/100)*35
        min_amt = int(min_amt1['default_bid_amount'])
        maxi = []
        if var>=len(membercount):
            data = "you can't participate in auction"
            return Response(data, status=status.HTTP_200_OK)
        if not min_amt<=int(bid_amount)<=max_amt:
            data="Enter the bid amount in range "+str(min_amt)+ " to "+str(max_amt)
            return Response(data, status=status.HTTP_200_OK)
        else:
            bid = Auctions.objects.filter(chit=chit).values_list('bid_amount')
            if bid:
                maxi = list(max(bid))
                if not int(maxi[0])<= int(bid_amount):
                    data = "Last highest bidded amount is " + str(maxi[0]) + ". Bid amount should be more than last highest bid, minimum 100 per bid(last highest bid + 100)"
                    return Response(data, status=status.HTTP_200_OK)
                elif not (int(maxi[0])+100)<= int(bid_amount):
                    data = "Minimum bid amount should be 100rs on last bid"
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    auct = Auctions()
                    auct.chit = chit
                    auct.foreman = foreman
                    auct.member = member
                    auct.bid_amount = bid_amount
                    auct.auctiondate = date1[0].auctiondate
                    auct.auction_call_date = datetime.datetime.now()
                    auct.save()
                    mem_count = FinalAuctions.objects.filter(chit=chit, member = str(member), flag = True).count()
                    presentId = FinalAuctions.objects.filter(chit=chit, flag = False).values().first()
                    FinalAuctions.objects.filter(id=presentId['id']).update(
                        foreman=request.data['foreman_id'],
                        member=str(member),
                        member_count=mem_count + 1
                    )
                    # fauct = FinalAuctions()
                    # fauct.chit = chit
                    # fauct.foreman = foreman
                    # fauct.member = member
                    # fauct.save()
                    data = "Bid Amount Succesfully Added"
                    return Response(data, status=status.HTTP_200_OK)
            else:
                auct = Auctions()
                auct.chit = chit
                auct.foreman = foreman
                auct.member = member
                auct.bid_amount = bid_amount
                auct.auctiondate = date1[0].auctiondate
                auct.auction_call_date = datetime.datetime.now()
                auct.save()
                mem_count = FinalAuctions.objects.filter(chit=chit, member=str(member), flag = True).count()
                presentId = FinalAuctions.objects.filter(chit=chit, flag = False).values().first()
                FinalAuctions.objects.filter(id = presentId['id']).update(
                    foreman=request.data['foreman_id'],
                    member=str(member),
                    member_count=mem_count + 1
                )
                # fauct = FinalAuctions()
                # fauct.chit = chit
                # fauct.foreman = foreman
                # fauct.member = member
                # fauct.save()
                data = "Bid Amount Succesfully Added"
                return Response(data, status=status.HTTP_200_OK)

class GetAuctionList(APIView):
    def post(self,request):
        print("zzzzzzzzzz#########", request.data)
        chit = request.data['id']
        list1 = []
        auction = Auctions.objects.filter(chit=chit)
        for i in auction:
            mem = MemberProfile.objects.filter(id=i.member)
            bidamount = i.bid_amount
            member_id = i.member
            data = {"member": mem[0].full_name, "bidamount": bidamount, "member_id": member_id,
                    "biddingtime": i.auction_call_date}
            list1.append(data)
        return Response(list1)

class Approve_auction_call_transaction(APIView):
    def post(self,request):
        userid = authentication(request.META['HTTP_AUTHORIZATION'])
        profile = ForemanProfile.objects.get(user=userid)
        print("sssssssssss",request.data)
        status1 = request.data['status']
        auction = request.data['auction']
        chit = request.data['chitid']
        if status1 == "VERIFIED":
            print ("hiiiiiiiiiiiiiii")
            Transactions.objects.filter(id=request.data['id1']).update(check=True)
        elif status1 == "UNVERFIED":
            Transactions.objects.filter(id=request.data['id1']).delete()
        elif status1 == "newid":
            if request.data['id1']:
                Transactions.objects.filter(id=request.data['id1']).update(transaction_id=request.data['newid'],check=True)
            else:
                a=Transactions()
                a.member=request.data['id']
                a.foreman=profile
                a.chit=request.data['chitid']
                a.transaction_id=request.data['newid']
                a.check=True
                a.auction=request.data['auction']
                a.mem_count=request.data['member_count']
                a.save()
        else:
            Transactions.objects.filter(id=request.data['id1']).update(check=None)
        transdata = Transactions.objects.filter(auction=auction,chit=chit)
        data2 = RunningChits.objects.filter(chit=chit).values_list('member', flat=True)
        data1 = Transactions.objects.filter(chit=chit,auction=auction).values_list('member', flat=True)
        datar = set(data2).union(data1)
        data3 = []
        for i in datar:
            member = MemberProfile.objects.filter(id=i)
            try:
                trans1 = Transactions.objects.filter(auction=auction, chit=chit, member=i)
                data1 = {"member_mobile_number": member[0].mobile_number, "membername": member[0].full_name,
                        "transaction_id": trans1[0].transaction_id, "check": trans1[0].check,"rtm_status":
                         trans1[0].rtm_status,"id":trans1[0].id,"auction_count":trans1[0].auction,"chit":trans1[0].chit}
                data3.append(data1)

            except:
                data1 = {"member_mobile_number": member[0].mobile_number, "membername": member[0].full_name}
                data3.append(data1)
        return Response(data3)


class Graph_details(APIView):
    def post(self,request):
        foreman_idss = authentication(request.META['HTTP_AUTHORIZATION'])
        chit_id = request.data['id']
        details = []
        chitinfo = Chits.objects.filter(id=chit_id)
        total_amount=chitinfo.values()
        finalcount = total_amount[0]['chit_duration']
        Foreman_comission = chitinfo.values_list('foreman_commission', flat=True)
        auction1 = FinalAuctions.objects.filter(chit=chit_id).order_by('auctiondate')
        temp = list(auction1)
        refchit = Chits.objects.filter(id=chit_id).values('chit_amount', 'foreman_id')[0]
        total_chit_amount=refchit['chit_amount']
        foreman_id=refchit['foreman_id']

        if MemberLoanDetails.objects.filter(chit=chit_id, member_id=foreman_idss, loan_type="Gold",
                                            status="Disbursed",
                                            payment_status="Pending"):
            loancheck = 'Present'
        else:
            print ("no")
            loancheck = 'None'

        for i in auction1:
            # aucdate = str(i.auctiondate)[:10]
            # Foremancomission = Foreman_comission[0]
            if (i.foreman == None) or (i.member==None):
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
                    print ("gtplllllllllll")
                    temp1 = int(i.auction_count) + 1
                    print("rrrrrrrrrrrrr"), temp1
                    nextpay = FinalAuctions.objects.filter(auction_count=temp1, chit=chit_id).values('payable_amount')
                    print("poooooo", nextpay[0]['payable_amount'])
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
                # final = FinalAuctions.objects.filter(chit=chit_id).values_list('auction_count',flat=True)
                # maxauction = max(final)
                balance1= FinalAuctions.objects.filter(chit=chit_id, auction_count=i.auction_count).values()
                dur = Chits.objects.get(id=chit_id)
                div = balance1[0]['balance_amount'] / dur.chit_duration
                divident_value = int(div)
                data = {"member": mem_name, "foreman": fore_name, "date": aucdate, "bidamount": bid_amount,
                        "nextpayableamount": payable_amount, "auctioncount": i.auction_count, "commission": comission,
                        "prizemoney": prize_money,"Foremancomission":Foremancomission ,"balance_amount":i.balance_amount,"dividend_value":divident_value,"next_date":i.next_date,"checking":foreman_idss,
                        "member_id":balance1[0]['member'],"loanchecking":loancheck}
                details.append(data)
            # print "detailsdetailsdetailsdetailsdetails",details
        return Response(details)


class FdUpload(APIView):
    def post(self,request):
        print("KKKKKKKKKK",request.data)
        try:
            id = authentication(request.META['HTTP_AUTHORIZATION'])
            foreman = ForemanProfile.objects.get(user = id)
            print("JJJJJJJ",foreman,request.data['chit'])
            data = Chits.objects.filter(id = request.data['chit'], foreman = foreman)
            print("LLLLLLL",data)

            if data:
                print("inside ifffffff")
                for key in request.data:
                    if key  == 'copy':
                        print ("inside copy",request.data['copy'])
                        data[0].fixeddepositcopy = request.data['copy']
                        data[0].save()
                        return Response("successfully uploded")
                    elif key == 'govt':
                        data[0].govtissuedcopy = request.data['govt']
                        data[0].save()
                        return Response("successfully uploded")
        except Exception as e:
            print("wwwwwwww",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Getupload(APIView):
    def get(self,request):
        print("dataaaaaaaaaaaaa",request.data)
        foremanid = authentication(request.META['HTTP_AUTHORIZATION'])
        print("foremanidddd",foremanid)
        doc = ForemanProfile.objects.get(user_id = foremanid)
        doc1=doc.id
        doc3=Chits.objects.filter(foreman_id=doc1).values()
        print("doc1111111111",doc3)
        print("aaaaaaaaaaaaaaaaaa",doc)
        return Response(doc3)

class MemberFundDetails(APIView):
    def post(self,request):
        print("reeeeeeqqqdadaaaaaaaaaaaaa",request.data)
        try:
            foremanid = authentication(request.META['HTTP_AUTHORIZATION'])
            foreman = ForemanProfile.objects.get(user_id = foremanid)
            id = request.data['chit_id']
            memid = list(RunningChits.objects.filter(chit = id).values())
            for i in memid:
                members = MemberProfile.objects.filter(id = i['member']).values()
                i['full_name'] = members[0]['full_name']
                i['city'] = members[0]['city']
                i['mobile_number'] = members[0]['mobile_number']

                tran1 = list(FinalAuctions.objects.filter(member=i['member'], chit=i['chit'],
                                                          member_count=i['member_count']).values())
                if tran1:
                    i['foreman_transaction'] = tran1[0]['foreman_transaction']
                    i['auction_count'] = tran1[0]['auction_count']
                    i['flag'] = tran1[0]['flag']
                else:
                    i['foreman_transaction'] = ''
                    i['auction_count'] = ''
                    i['flag'] = ''

            return Response(memid)
        except Exception as e:
            print(e)
            return Response('failed',status=status.HTTP_400_BAD_REQUEST)



class ViewMemberProfile(APIView):
    def post(self,request):
        try:
            print("reeeeeeeeeeeeeeeeeeeeeeeee",request.data)
            id  = request.data['data']
            print("idddddddddddddddddddddddd",id)
            memdata = MemberProfile.objects.filter(id  = id).values()
            print("idddddddddddddddddddddddd",memdata)

            return Response(memdata)
        except Exception as e:
            print(e)



class ForemanPicUpdated(APIView):
    def post(self,request):
        print("ggggggggggg", request.data['fpic'])
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        print("aaaaaaaaaaaaa", id)
        user = ForemanProfile.objects.get(user = id)
        print("8888888888888888888", user)
        user.front_photo = request.data['fpic']
        user.save()
        return Response("kkkkkkkk")


class GetForemanPic(APIView):
    def get(self,request):
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        print("aaaaaaaaaaaaa", id)
        user = ForemanProfile.objects.filter(user = id)
        print("8888888888888888888", user)
        data1 = {
            'front_pic' : user[0].front_photo.url,
        }
        return Response(data1)


class SaveTransaction(APIView):
    def post(self,request):
        print("@@@@@@@@@",request.data)
        id = authentication(request.META['HTTP_AUTHORIZATION'])
        chit_id = request.data['Chit_ID']
        memberCount = request.data['memberID']
        auctionNo = request.data['auctionId']
        tran = FinalAuctions.objects.get(chit=chit_id,member_count=memberCount,flag= True,auction_count = auctionNo)
        print("***********",tran)
        tran.foreman_transaction = request.data['transaction']
        tran.foreman_transaction_status = 'Done'
        tran.save()
        return Response("Data Added")

class ForemanClosedChits(APIView):
    def get(self,request):
        print('pppppppppppppppppp',request.data)
        try:
            profile = authentication(request.META['HTTP_AUTHORIZATION'])
            print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", profile)
            chit_count = Chits.objects.filter(status="CLOSED").count()
            print("yyyyyyyyyyyyyyyyyyyyy",chit_count)
            chits = Chits.objects.filter(status="CLOSED").order_by('-id')
            print("nnnnnnnnnnnnnnnnnn", chits)
            chits_dict = chits.values()
            print('sssssssssss', chits_dict)
            for idx, chit_dict in enumerate(chits_dict):
                chit_dict['company_logo'] = chits[idx].company_logo.url
            return Response({'data': chits_dict, 'chit_count': chit_count}, status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



