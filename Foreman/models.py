# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from Gfundsbackend2 import settings

# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class ForemanProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.CharField(max_length=50, primary_key=True)
    full_name = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.TextField(null=True, blank=True)
    role = models.TextField(default="foreman")
    email_id = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    aadhaar_card = models.CharField(max_length=100, null=True, blank=True)
    applicant_pancard_number = models.CharField(max_length=50, null=True, blank=True)
    district = models.TextField(null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    spouse_name = models.CharField(max_length=50, null=True, blank=True)
    present_address_type = models.CharField(max_length=50, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)
    building_name = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    home_land_mark = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.PositiveIntegerField(null=True, blank=True)
    present_city = models.CharField(max_length=100, null=True, blank=True)
    present_district = models.CharField(max_length=100, null=True, blank=True)
    present_state = models.CharField(max_length=100, null=True, blank=True)
    address_proof = models.FileField('addressProof', upload_to=upload_location,
                                     storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    employment_type = models.CharField(max_length=50, null=True, blank=True)
    organization_type = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    company_landmark = models.CharField(max_length=100, null=True, blank=True)
    annual_salary = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    bank_statement = models.FileField('bankstatement', upload_to=upload_location,
                                      storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    business_entity_type = models.CharField(max_length=100, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.CharField(max_length=100, null=True, blank=True)
    business_landmark = models.CharField(max_length=100, null=True, blank=True)
    business_pincode = models.TextField(null=True, blank=True)
    industry_type = models.CharField(max_length=50, null=True, blank=True)
    company_pancard_number = models.CharField(max_length=50, null=True, blank=True)
    employee_id_card = models.FileField('EmployeeIdCard', upload_to=upload_location,
                                       storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    certificate_of_registration = models.FileField('certificateOfRegistration', upload_to=upload_location,
                                                   storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                                                   null=True, blank=True)
    business_bank_statement = models.FileField('businessBankStatement', upload_to=upload_location,
                                               storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True,
                                               blank=True)
    company_pancard = models.FileField('companyPancard', upload_to=upload_location,
                                       storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    company_address_proof = models.FileField('companyAddressProof', upload_to=upload_location,
                                             storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True,
                                             blank=True)
    office_contact_number = models.TextField(null=True, blank=True)
    partner_name = models.CharField(max_length=50, null=True, blank=True)
    partner_contact_number = models.TextField(null=True, blank=True)
    about_us = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=20, null=True, blank=True)
    branch_name = models.CharField(max_length=20, null=True, blank=True)
    ifsc_code = models.CharField(max_length=11, null=True, blank=True)
    account_name = models.CharField(max_length=50, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    account_type = models.CharField(max_length=50, null=True, blank=True)
    agree = models.NullBooleanField(default=False)
    bank_statement_datetime_creation = models.DateField(null=True, blank=True)
    bank_statement_datetime_modified = models.DateField(null=True, blank=True)
    aggrement = models.FileField('aggrement', upload_to=upload_location,
                                 storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    front_photo = models.FileField('Photo Front', upload_to=upload_location,
                                   storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    chit_company = models.CharField(max_length=500, null=True, blank=True)
    chit_company_address = models.CharField(max_length=100, null=True, blank=True)
    chit_company_landmark = models.CharField(max_length=100, null=True, blank=True)
    chit_company_logo = models.FileField('Logo', upload_to=upload_location,
                                         storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    chit_company_licence = models.FileField('licence', upload_to=upload_location,
                                            storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True,
                                            blank=True)
    transaction_id = models.TextField(blank=True, null=True)
    transaction_verify = models.BooleanField(default = False)
    foreman_deposit_amount = models.CharField(max_length=100, null=True, blank=True)
    gchits_score = models.IntegerField(default=0, null=True, blank=True)
    device_token = models.TextField(null=True, blank=True)
    is_active = models.NullBooleanField(default=False)
    foreman_rating = models.IntegerField(default=0, null=True, blank=True)
    chit_company_estd = models.IntegerField(default=0,null=True,blank=True)


    def __str__(self):
        return self.id

class Chits(models.Model):
    foreman = models.ForeignKey(ForemanProfile,on_delete=models.CASCADE)
    chit_number = models.CharField(max_length=50, null=True, blank=True)
    chit_type = models.CharField(max_length=50, null=True, blank=True)
    chit_amount = models.IntegerField(null=True, blank=True)
    chit_duration = models.IntegerField(null=True, blank=True)
    max_bid_amount = models.IntegerField(null=True, blank=True)
    min_bid_amount = models.IntegerField(null=True, blank=True)
    chit_location = models.CharField(max_length=100, null=True, blank=True)
    foreman_commission = models.IntegerField(null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    company_logo = models.FileField('Logo', upload_to=upload_location,
                                    storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)
    prize_money = models.IntegerField(null=True, blank=True)
    amount_in_string = models.TextField(null=True, blank=True)
    duration_in_string = models.TextField(null=True, blank=True)
    status = models.TextField(default="UPCOMING", null=True, blank=True)
    chit_score = models.TextField(null=True, blank=True)
    check = models.NullBooleanField(default=False)
    startdate = models.DateField(null=True,blank=True)
    premium_amount = models.IntegerField(null=True, blank=True)
    fixeddepositcopy = models.FileField('Deposit_copy',
                                        upload_to=upload_location,
                                        storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)

    govtissuedcopy = models.FileField('Deposit_copy',
                                      upload_to=upload_location,
                                      storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True)

    def __str__(self):
        return str(self.id)




class RunningChits(models.Model):
    foreman = models.TextField()
    member = models.TextField()
    chit = models.TextField()
    amount = models.TextField(null=True, blank=True)
    transcationid = models.TextField(null=True, blank=True)
    depdate = models.DateField(null=True, blank=True)
    membercheck = models.TextField(null=True, blank=True)
    auctiondate = models.DateTimeField(null=True, blank=True)
    auction_number = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    trans_verify = models.NullBooleanField()
    member_count = models.IntegerField(null=True,blank=True)
    added_member_status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)

class Auctions(models.Model):
    foreman = models.TextField(null=True, blank=True)
    member = models.TextField(null=True, blank=True)
    chit = models.TextField(null=True, blank=True)
    auctiondate = models.DateTimeField(null=True, blank=True)
    bid_amount = models.IntegerField(null=True, blank=True)
    member_status = models.BooleanField(default=False)
    auction_call_date = models.DateTimeField(null=True, blank=True)

class FinalAuctions(models.Model):
    foreman = models.TextField(null=True, blank=True)
    member = models.TextField(null=True, blank=True)
    chit = models.TextField(null=True, blank=True)
    auctiondate = models.DateTimeField(null=True, blank=True)
    next_date = models.DateTimeField(null=True, blank=True)
    bid_amount = models.TextField(null=True, blank=True)
    payable_amount = models.IntegerField(null=True, blank=True)
    member_status = models.BooleanField(default=False)
    auction_count = models.TextField(null=True, blank=True)
    receiving_member_amount = models.TextField(null=True, blank=True)
    foreman_platform_comission = models.IntegerField(null=True,blank=True)
    platform_comission = models.IntegerField(null=True,blank=True)
    reseller_comission = models.IntegerField(null=True,blank=True)
    balance_amount = models.IntegerField(default=0, null=True,blank=True)
    foreman_transaction = models.TextField(null=True, blank=True)
    foreman_transaction_status = models.TextField(null=True, blank=True)
    default_bid_amount = models.TextField(null=True, blank=True)
    default_chit_amount = models.TextField(null=True, blank=True)
    flag = models.BooleanField(default=False)
    member_count = models.IntegerField(blank=True,null=True)