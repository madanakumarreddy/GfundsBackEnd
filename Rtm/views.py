import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework .views import APIView
# Create your views here.
from Members.functions import authentication
from Members.models import Transactions,MemberProfile
from Rtm.models import Loan, MemberLoanDetails
from Rtm.models import DefaultInterestCharges
from Foreman.models import Chits,FinalAuctions, RunningChits,ForemanProfile
from dateutil.relativedelta import relativedelta



class RaiseLoan(APIView):
    def post(self,request):
        # newloan = request.data.values()
        # print("asssssssssssssssssss",newloan)
        try:
            userid=authentication(request.META['HTTP_AUTHORIZATION'])
            print('whoisthat',userid)
            print("777777777777777",request.data)
            try:
                print("hiiiiiiiiiiiii")
                foreman = ForemanProfile.objects.get(user = userid)
                print("99999999999999")
                data=request.data
                print("ffffffffffffdattttttttttttatttttaaaa",data,type(data))
                # print("dataaaa",data)
                member_id= foreman
                print("memme",member_id)
                chit_id=data['chitid']
                print("citttttttttttttttttt",chit_id)
                member = MemberProfile.objects.get(id=data['id'])
                loan=Loan.objects.filter(member=member,chit=chit_id,mem_count=request.data['member_count'])
                interest=DefaultInterestCharges.objects.filter(is_active=True,loan_type='Platinum').values()
                print("intttttttttttttteeeeeeeeeeee",interest,loan)
                chits = Chits.objects.filter(id = chit_id).values_list('chit_duration',flat=True)
                print("chitttttttttttttttttttttttt",chits)
                finaldata = FinalAuctions.objects.filter(member = member,chit = chit_id, member_count = request.data['member_count'])
                print("finnnnnnnnnnnnnnnnnnnn",finaldata)

                if not finaldata:
                    sildata = FinalAuctions.objects.filter(chit = chit_id, auction_count = request.data['auction']).values('payable_amount')
                    print("sivvvvvvvvvvvvvvvvvv",sildata)
                    payable = sildata[0]['payable_amount']
                    print("paaaaaaaaaaaaaaaa",payable)
                    data['loan_type'] = 'Silver'
                    print("222222222222222222",data['loan_type'])
                    print("888888888@@@@@@@",data['loan_type'])
                    data['insurance'] = 0
                    data['processing_fees'] = 0
                    data['member_fees'] = 0
                    data['selected_interest'] = interest[0]['interest']

                else:
                    print("elseeeeeeeeee 888888888888")
                    sildata = FinalAuctions.objects.filter(chit = chit_id, auction_count = request.data['auction']).values('payable_amount')
                    print("sannnnnnnnnnnnnnnnn",sildata)
                    payable = sildata[0]['payable_amount']
                    print("paidddddddddddplaaaaaaaaaaaaaaaaaaa",payable)
                    data['loan_type'] = "Platinum"
                    print("#################",data['loan_type'])
                    data['insurance'] = interest[0]['insurance']
                    data['processing_fees'] = interest[0]['processing_fees']
                    data['member_fees'] = interest[0]['member_fees']
                    data['selected_interest'] = interest[0]['interest']

                loan = Loan()
                print("LOANNNNNNNNNNNN",loan)
                loan.member_id = member
                loan.chit = chit_id
                print("6666666666",data['loan_type'],type(data['loan_type']))
                loan.loan_type = data['loan_type']
                loan.member_mobile_number = data['member'][0]['mobile_number']
                loan.auction_count = data['auction']
                loan.member_name = data['member'][0]['full_name']
                loan.tenure = data['chit_duration']
                loan.loan_amount = payable
                loan.foreman = foreman
                loan.selected_interest = data['selected_interest']
                loan.processing_fee = data['processing_fees']
                loan.membership_fee = data['member_fees']
                loan.insurance = data['insurance']
                loan.mem_count = data['member_count']
                print("hiiiiiiiiiiiiiiii")
                loan.save()
                return Response("Loan Has Been Raised Sucessfully Raised")

                member_transaction = Transactions()
                member_transaction.member = id
                member_transaction.foreman = foreman
                member_transaction.chit = chit_id
                member_transaction.auction = data['auction']
                member_transaction.rtm_status = False
                member_transaction.mem_count = data['member_count']
                member_transaction.save()
                return Response("successfully saved")
            except ForemanProfile.DoesNotExist:
                print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                foreman = MemberProfile.objects.get(user = userid)
                data = request.data
                chit = data['chit']
                mem = MemberProfile.objects.filter(id=foreman).values("full_name", "mobile_number")
                chitduration = Chits.objects.filter(id=chit).values("chit_duration", "foreman_id")
                mem[0]['full_name'], chitduration[0]['chit_duration'], chitduration[0]['foreman_id']
                finalmemdata = FinalAuctions.objects.filter(chit=chit, member=foreman).values_list('member_count',
                                                                                                    flat=True)
                rundata = RunningChits.objects.filter(chit=chit, member=foreman).values_list('member_count', flat=True)
                li = list(set(rundata) - set(finalmemdata))
                loangold = Loan.objects.filter(chit=chit, member_id=foreman, loan_type='Gold').values_list('mem_count',
                                                                                                            flat=True)
                golddata = list(set(rundata) - set(loangold))
                finalgold = list(set(li) & set(golddata))
                if finalgold:
                    loan1 = Loan()
                    loan1.member_id = foreman
                    loan1.chit = data['chit']
                    loan1.loan_type = data['loan_type']
                    loan1.member_mobile_number = mem[0]['mobile_number']
                    loan1.auction_count = data['auction_count']
                    loan1.member_name = mem[0]['full_name']
                    loan1.tenure = chitduration[0]['chit_duration']
                    loan1.loan_amount = data['loan_amount']
                    loan1.foreman = chitduration[0]['foreman_id']
                    loan1.selected_interest = 0
                    loan1.processing_fee = 0
                    loan1.membership_fee = 0
                    loan1.insurance = 0
                    loan1.mem_count = finalgold[0]
                    loan1.save()
                    return Response("successfully saved", status=status.HTTP_200_OK)
                else:
                    return Response("you have already taken gold loan")
        except Exception as e:
            print(e)
        return Response("llllllll", status=status.HTTP_400_BAD_REQUEST)


class Request_loan(APIView):
    def get(self,request):
            user = authentication(request.META['HTTP_AUTHORIZATION'])
            print("uuuuuuuuuuuuuuuuuuu",user)
            if user:
                loan = Loan.objects.filter(status='Accepted').values()
                return Response(loan)
            else:
                return Response("Invalid User")


class Approve_req(APIView):
     def post(self,request):
         print("fromfront",request.data)
         data=request.data
         today=datetime.date.today()
         next_date=today+relativedelta(months=1)
         loan_amount=request.data['loandetail'][0]['loan_amount']
         # loan_amount1=float[loan_amount]
         print("loanamountt",loan_amount)
         id=request.data['loandetail'][0]['id']
         print("idddd",id)
         loan_type=request.data['loandetail'][0]['loan_type']
         tenure=request.data['loandetail'][0]['tenure']
         auction_count=request.data['loandetail'][0]['auction_count']
         iteration = int(tenure) + 1
         chit=request.data['loandetail'][0]['chit']
         transaction_id=request.data['popdata']
         member=request.data['loandetail'][0]['member_id']
         loan=Loan.objects.filter(member=member,auction_count=auction_count,chit=chit).values()
         print("loannnnnnnnnnnnnnnnnn",loan)
         interest=(float(loan[0]['loan_amount'])*float(loan[0]['selected_interest']))/100
         print("interestttttttt",interest)
         loan1=loan.update(interest_amount=interest)
         print("l1111111111111111111",loan1)
         total_return_amount=loan_amount + (float(loan[0]['processing_fee']) + float(loan[0]['insurance'])  + float(loan[0]['membership_fee']))
         print("totalllllllll",total_return_amount)
         loan = Loan.objects.filter(member_id=member, id=id, chit=chit, mem_count=request.data['loandetail'][0]['mem_count']).update(status="Disbursed", disbursed_date=today,
             payable_date=next_date)
         print("loannnnnndettttt",loan)
         finalauction=FinalAuctions.objects.filter(chit=chit).values('payable_amount', 'auction_count')
         loan=Loan.objects.filter(chit=chit,member_id=member).values('member_name')
         data=MemberLoanDetails.objects.filter(chit=chit,member_id=member,member_count=request.data['loandetail'][0]['mem_count']).values()
         for k in finalauction:
             for i in range(1, iteration):
                 if i == iteration - 1:
                     if not data:
                         details = MemberLoanDetails()
                         details.auction_count = k['auction_count']
                         details.id = MemberLoanDetails.objects.all().count() + 1
                         details.payable_amount = k['payable_amount']
                         details.loan_amount = loan_amount
                         details.chit = chit
                         details.member_name = loan[0]['member_name']
                         details.tenure = tenure
                         details.member_id = member
                         details.member_count = request.data['loandetail'][0]['mem_count']
                         details.save()

                         MemberLoanDetails.objects.filter(auction_count=auction_count, member_id=member,
                                                          chit=chit, member_count=request.data['loandetail'][0]['mem_count']).update(
                             chit_loan_amount=loan_amount, disbursed_date=today, transaction_id=transaction_id,
                             status="Disbursed", payable_date=next_date, rtm_status="RTM", loan_type=loan_type,
                             payable_amount=total_return_amount)
                     else:
                         data1 = MemberLoanDetails.objects.filter(chit=chit, member_id=member,
                                                                  member_count=request.data['loandetail'][0]['mem_count']).values()
                         for j in data1:
                             if j['member_id'] == member and j['chit'] == chit and j['auction_count'] == auction_count:
                                 data = MemberLoanDetails.objects.filter(auction_count=auction_count, member_id=member,
                                                                         chit=chit, member_count=request.data['loandetail'][0]['mem_count']).update(
                                     chit_loan_amount=loan_amount, disbursed_date=today, transaction_id=transaction_id,
                                     status="Disbursed", payable_date=next_date, rtm_status="RTM", loan_type=loan_type,
                                     payable_amount=total_return_amount)
         Transactions.objects.filter(foreman=request.data['loandetail'][0]['foreman'], chit=chit, auction=auction_count,
                                     member=member, mem_count=request.data['loandetail'][0]['mem_count']).update(
             transaction_id=transaction_id, trans_date=datetime.datetime.now(), rtm_status=True,check=None)
         return Response('wwwwwwwwwwwwwwwwsuccesfully saved', status=status.HTTP_200_OK)


class Getsilverloan(APIView):
    def get(self,request):
        data1=MemberLoanDetails.objects.filter(status='Disbursed',loan_type='Silver').values('member_count','chit','member_id','payable_amount','loan_type','member_name','disbursed_date')
        return Response(data1)

class Getplatinumloan(APIView):
    def get(self,request):
        data1=MemberLoanDetails.objects.filter(status='Disbursed',loan_type='Platinum').values('member_count','chit','member_id','payable_amount','loan_type','member_name','disbursed_date')
        return Response(data1)

class Getgoldloan(APIView):
    def get(self,request):
        data1=MemberLoanDetails.objects.filter(status='Disbursed',loan_type='Gold').values('member_count','chit','member_id','payable_amount','loan_type','member_name','disbursed_date')
        return Response(data1)
























