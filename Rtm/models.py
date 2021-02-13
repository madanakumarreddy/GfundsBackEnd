from django.db import models


from Members.models import MemberProfile



class Loan(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete = models.CASCADE)
    member_mobile_number = models.TextField(null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tenure = models.IntegerField(null=True, blank=True)
    status = models.CharField(default="Accepted", max_length=120, null=True, blank=True)
    processing_fee = models.DecimalField(default=0,max_digits=15, decimal_places=2, null=True, blank=True)
    requested_date = models.DateField(auto_now_add=True, null=True, blank=True)
    disbursed_date = models.DateField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)
    membership_fee = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    insurance = models.DecimalField(default=0,max_digits=15, decimal_places=2, null=True, blank=True)
    accepted_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_return_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    member_transaction_id = models.CharField(max_length=50, null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True, default=0)
    total_paid_amount=models.IntegerField(null=True,default=0)
    pending_amount=models.IntegerField(null=True,default=0)
    chit=models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(default="Pending", max_length=120, null=True, blank=True)
    penalty = models.IntegerField(null=True, blank=True, default=0)
    payable_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    loan_type=models.CharField(max_length=20,null=True,blank=True)
    loan_id = models.IntegerField(null=True, blank=True)
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_amount=models.IntegerField(null=True,default=0)
    pricemoney_status=models.CharField(default='No',max_length=20)
    member_name = models.CharField(max_length=50, null=True, blank=True)
    auction_count = models.TextField(null=True, blank=True)
    chit_amount = models.IntegerField(null=True, blank=True)
    selected_interest = models.TextField(null=True, blank=True)
    foreman = models.TextField(null=True, blank=True)
    mem_count = models.IntegerField(null=True,blank=True)


class DefaultInterestCharges(models.Model):
    interest = models.IntegerField(null=True,default=0)
    processing_fees = models.DecimalField(max_digits=6, decimal_places=2)
    member_fees = models.DecimalField(max_digits=6, decimal_places=2)
    insurance = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=False)
    loan_type = models.CharField(max_length=200, null=True, blank=True)



class MemberLoanDetails(models.Model):
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(default="Accepted", max_length=120, null=True, blank=True)
    disbursed_date = models.DateField(null=True, blank=True)
    disbursed_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)
    repayment_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payable_amount = models.IntegerField(default=0)
    penalty_amount = models.IntegerField(default=0)
    payable_date = models.DateField(null=True, blank=True)
    payment_status = models.TextField(default="Pending")
    tenure = models.IntegerField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    payment_mode = models.TextField(null=True,blank=True)
    chit = models.CharField(max_length=50, null=True, blank=True)
    auction_count = models.TextField(null=True, blank=True)
    member_id = models.TextField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True, default=0)
    chit_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    member_name = models.CharField(max_length=50, null=True, blank=True)
    rtm_status = models.CharField(max_length=50, null=True, blank=True,default="Member")
    loan_type=models.CharField(max_length=20,null=True,blank=True)
    gfund_transaction_id=models.CharField(max_length=100, null=True, blank=True)
    member_count = models.IntegerField(null=True,blank=True)

