# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from Gfundsbackend2 import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import datetime


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class MemberProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.CharField(max_length=50, primary_key=True)
    full_name = models.TextField(null=True, blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.TextField(unique=True, null=True, blank=True, default="")
    role = models.TextField(default="member")

    '''####################  Profile  ##############################'''
    gender = models.CharField("Gender",max_length=10, null=True, blank=True, default="")
    # full_name = models.CharField('Full Name', max_length=120, null=True, blank=True)
    pancard_number = models.CharField(max_length=50, null=True, blank=True, default="")
    aadhaar_card = models.CharField(max_length=100, null=True, blank=True, default="")
    qualification = models.CharField(max_length=50, null=True, blank=True, default="")
    smart_phone = models.TextField(null=True, blank=True, default="")
    religion = models.TextField(null=True, blank=True, default="")
    email_id = models.EmailField(null=True, blank=True, default="")

    # marital status
    marital_status = models.CharField(max_length=20, null=True, blank=True, default="")
    spouse_name = models.CharField(max_length=20, null=True, blank=True, default="")
    spouse_number = models.TextField(null=True, blank=True, default="")
    dat_of_marriage = models.DateField(null=True, blank=True)
    spouse_work = models.CharField(max_length=20, null=True, blank=True, default="")
    seperated_since = models.CharField(max_length=50, null=True, blank=True, default="")

    # Fathers details for unmarried
    father_name = models.CharField(max_length=255, null=True, blank=True, default="")

    #nominee status
    nominee_name=models.CharField(max_length=200,null=True,blank=True, default="")
    nominee_age=models.IntegerField(null=True,blank=True, default=0)
    nominee_relationship=models.CharField(max_length=150,blank=True, default="")

    # present address
    present_address_type = models.CharField(max_length=100, null=True, blank=True, default="")
    house_no = models.CharField('Flat No.', max_length=200, null=True, blank=True, default="")
    building_name = models.CharField('Bulding/ Apartment Name', max_length=120, default=1, null=True, blank=True)
    street = models.CharField('Street', max_length=120, null=True, blank=True, default="")
    landmark = models.CharField('Landmark', max_length=120, null=True, blank=True, default="")
    pincode = models.IntegerField(null=True, blank=True, default=0)
    district = models.CharField('District', max_length=120, null=True, blank=True, default="")
    city = models.TextField(null=True, blank=True, default="")
    state = models.TextField(null=True, blank=True, default="")
    staying_from = models.CharField(max_length=50, null=True, blank=True, default="")

    # permanent address
    permanent_address = models.CharField(max_length=100, null=True, blank=True, default="")
    permanent_houseno = models.CharField('Flat No.', max_length=200, null=True, blank=True, default="")
    permanent_housename = models.CharField('Bulding/ Apartment Name', max_length=120, default=1, null=True, blank=True)
    permanent_street = models.CharField('Street', max_length=120, null=True, blank=True, default="")
    permanent_landmark = models.CharField('Landmark', max_length=120, null=True, blank=True, default="")
    permanent_pincode = models.IntegerField(null=True, blank=True, default=0)
    permanent_district = models.CharField('District', max_length=120, null=True, blank=True, default="")
    permanent_city = models.TextField(null=True, blank=True, default="")
    permanent_state = models.TextField(null=True, blank=True, default="")
    present_address_proof = models.FileField('Address Proof(Light Bill, Passport)',
                                             upload_to=upload_location,
                                             storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True,
                                             blank=True, default="")

    # employment type
    profession = models.CharField(max_length=50, null=True, blank=True, default="")
    are_you_in = models.TextField(null=True, blank=True, default="")
    job = models.TextField(null=True, blank=True, default="")

    # salaried
    organization_name = models.CharField(max_length=500, null=True, blank=True, default="")
    designation = models.CharField(max_length=200, null=True, blank=True, default="")
    id_card_number = models.CharField(max_length=50, null=True, blank=True, default="")
    employe_id_card = models.FileField('Employe Id Card',
                                       upload_to=upload_location,
                                       storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    pay_slip1 = models.FileField('Upload 1months Payslip', upload_to=upload_location,
                                 storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    pay_slip2 = models.FileField('Upload 2months Payslip', upload_to=upload_location,
                                 storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    pay_slip3 = models.FileField('Upload 3months Payslip', upload_to=upload_location,
                                 storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    purpose_of_loan = models.CharField(max_length=50, null=True, blank=True, default="")
    bank_statement = models.FileField('Bank Statment',
                                      upload_to=upload_location,
                                      storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    bank_statement_upload_time = models.DateTimeField(null=True, blank=True)

    # self employeed and shop owner
    shop_name = models.TextField(null=True, blank=True, default="")
    shop_address = models.TextField(null=True, blank=True, default="")
    contact_phone_number = models.TextField(null=True, blank=True, default="")
    branch_office = models.CharField(max_length=50, null=True, blank=True, default="")

    # self employeed  and   smallbusiness
    busines_type = models.CharField('Business Type', max_length=120, null=True, blank=True, default="")
    busines_name = models.CharField('Business Name', max_length=120, null=True, blank=True, default="")
    industry_type = models.CharField('Industry Type', max_length=100, null=True, blank=True, default="")
    busines_loc = models.CharField('Business Location', max_length=120, null=True, blank=True, default="")
    busines_landmark = models.CharField('Landmark', max_length=120, null=True, blank=True, default="")
    busines_city = models.CharField(max_length=30, null=True, blank=True, default="")
    busines_district = models.CharField(max_length=30, null=True, blank=True, default="")
    busines_pincode = models.IntegerField(null=True, blank=True, default=0)
    busines_state = models.CharField(max_length=30, null=True, blank=True, default="")
    no_of_employees = models.CharField(max_length=50, null=True, blank=True, default="")
    year_of_estd = models.DateField(null=True, blank=True)
    turn_over = models.IntegerField(null=True, blank=True, default=0)
    partner_name = models.CharField(max_length=100, null=True, blank=True, default="")
    din = models.IntegerField(null=True, blank=True, default=0)
    company_pan = models.TextField(null=True, blank=True, default="")
    self_income = models.TextField(null=True, blank=True, default="")
    bank_balance = models.TextField(null=True, blank=True, default="")
    itreturn = models.FileField('Last Year IT returns',
                                upload_to=upload_location,
                                storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    business_adressproof = models.FileField('Business Addressd', upload_to=upload_location,
                                            storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True,
                                            blank=True, default="")

    # are you an incometax payer
    incometaxpayer = models.TextField(blank=True, default="" , null=True)

    # Introduced By:
    introduceby = models.CharField(null=True, blank=True, max_length=255, default="")

    # References:
    refname1 = models.CharField(null=True, blank=True, max_length=255, default="")
    refphone_number1= models.TextField(null=True, blank=True, default="")
    refname2 = models.CharField(null=True, blank=True, max_length=255, default="")
    refphone_number2 = models.TextField(null=True, blank=True, default="")


    # Immovable Properties
    property = models.CharField(max_length=20, null=True, blank=True, default="")

    # current loan details
    running_loans = models.TextField(null=True, blank=True, default="")
    running_two_wheeler_loan = models.CharField(max_length=20, null=True, blank=True, default="")
    two_wheeler_bank = models.CharField(max_length=50, null=True, blank=True, default="")

    # twowheelerotherbank = models.CharField(max_length=50, null=True, blank=True)
    two_wheeler_emi = models.CharField(max_length=30, null=True, blank=True, default="")
    two_wheeler_tenure = models.CharField(max_length=30, null=True, blank=True, default="")
    two_wheeler_emi_left = models.CharField(max_length=30, null=True, blank=True, default="")

    running_four_wheeler_loan = models.CharField(max_length=20, null=True, blank=True, default="")
    four_wheeler_bank = models.CharField(max_length=50, null=True, blank=True, default="")

    # fourwheelerotherbank = models.CharField(max_length=50, null=True, blank=True)
    four_wheeler_emi = models.CharField(max_length=30, null=True, blank=True, default="")
    four_wheeler_tenure = models.CharField(max_length=30, null=True, blank=True, default="")
    four_wheeler_emi_left = models.CharField(max_length=30, null=True, blank=True, default="")

    running_personal_loan = models.CharField(max_length=30, null=True, blank=True, default="")
    personal_bank = models.CharField(max_length=50, null=True, blank=True, default="")

    # personalotherbank = models.CharField(max_length=50, null=True, blank=True)
    personal_emi = models.CharField(max_length=30, null=True, blank=True, default="")
    personal_tenure = models.CharField(max_length=30, null=True, blank=True, default="")
    personal_emi_left = models.CharField(max_length=30, null=True, blank=True, default="")

    running_home_loan = models.CharField(max_length=30, null=True, blank=True, default="")
    home_bank = models.CharField(max_length=50, null=True, blank=True, default="")

    # homeotherbank = models.CharField(max_length=50, null=True, blank=True)
    home_emi = models.CharField(max_length=30, null=True, blank=True, default="")
    home_tenure = models.CharField(max_length=30, null=True, blank=True, default="")
    home_emi_left = models.CharField(max_length=30, null=True, blank=True, default="")

    any_other_loan = models.CharField(max_length=10, null=True, blank=True, default="")
    other_bank = models.CharField(max_length=50, null=True, blank=True, default="")
    loan_name = models.CharField(max_length=50, null=True, blank=True, default="")
    other_emi = models.CharField(max_length=30, null=True, blank=True, default="")
    other_tenure = models.CharField(max_length=30, null=True, blank=True, default="")
    other_emi_left = models.CharField(max_length=30, null=True, blank=True, default="")

    # bank details
    selected_bank = models.CharField(max_length=500, null=True, blank=True, default="")
    holder_name = models.CharField(max_length=50, null=True, blank=True, default="")
    account_number = models.CharField(max_length=50, null=True, blank=True, default="")
    account_type = models.CharField(max_length=50, null=True, blank=True, default="")
    branch_name = models.CharField(max_length=50, null=True, blank=True, default="")
    ifsc_code = models.CharField(max_length=30, null=True, blank=True, default="")
    mode_of_salary = models.CharField(max_length=30, null=True, blank=True, default="")
    about_gchits = models.CharField(max_length=50, null=True, blank=True, default="")
    time_to_contact = models.CharField(max_length=30, null=True, blank=True, default="")
    alternate_number = models.TextField(null=True, blank=True, default="")
    front_photo = models.FileField('Photo Front', upload_to=upload_location,
                                   storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")

    payslip_datetime_creation1 = models.DateTimeField(null=True, blank=True)
    payslip_datetime_modified1 = models.DateTimeField(null=True, blank=True)

    payslip_datetime_creation2 = models.DateTimeField(null=True, blank=True)
    payslip_datetime_modified2 = models.DateTimeField(null=True, blank=True)

    payslip_datetime_creation3 = models.DateTimeField(null=True, blank=True)
    payslip_datetime_modified3 = models.DateTimeField(null=True, blank=True)

    # gchits score and credit limit
    credit_limit = models.IntegerField(default=0, null=True, blank=True)
    loan_availed = models.IntegerField(default=0, null=True, blank=True)
    available_amount = models.IntegerField(default=0, null=True, blank=True)
    gchits_score = models.IntegerField(default=0, null=True, blank=True)
    joined_date = models.DateField(default=datetime.date.today, null=True, blank=True)
    cibil_score = models.IntegerField(default=0, null=True, blank=True)
    cibil_score_file=models.FileField('proof', upload_to=upload_location,
                                   storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default='M4/cibil_file.jpg')
    member_rating = models.IntegerField(default=0, null=True, blank=True)

    # pan_image
    panimage=models.FileField('panimage',
                              upload_to=upload_location,
                              storage=FileSystemStorage(location=settings.MEDIA_ROOT),null=True,blank=True, default="")

#Aadhar_image
    aadharimage = models.FileField('aadharimage',
                                   upload_to=upload_location,
                                   storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")


    #Agrement file

    agrementcopy = models.FileField('Agreement_form',
                                      upload_to=upload_location,
                                      storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")

    rtmagrementcopy = models.FileField('Agreement_form',
                                    upload_to=upload_location,
                                    storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")
    addagrementcopy = models.FileField('Agreement_form',
                                       upload_to=upload_location,
                                       storage=FileSystemStorage(location=settings.MEDIA_ROOT), null=True, blank=True, default="")

    # Verification
    profile_update = models.BooleanField(default=False)
    verify_present_address_proof = models.BooleanField(default=False)
    verify_employee_id_card = models.BooleanField(default=False)
    verify_pay_slip1 = models.BooleanField(default=False)
    verify_pay_slip2 = models.BooleanField(default=False)
    verify_pay_slip3 = models.BooleanField(default=False)
    verify_bank_statement = models.BooleanField(default=False)
    verify_itreturn = models.BooleanField(default=False)
    verify_business_address_proof = models.BooleanField(default=False)
    device_token = models.TextField(null=True, blank=True, default="")
    is_active = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.id

class Request(models.Model):
    member_id = models.TextField(null=True, blank=True)
    member_name = models.TextField(null=True, blank=True)
    member_number = models.TextField(null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    credit = models.TextField(null=True, blank=True)
    foreman_id = models.TextField(null=True, blank=True)
    foreman_name = models.TextField(null=True, blank=True)
    foreman_number = models.TextField(null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    chit_name = models.TextField(null=True, blank=True)
    chit_id = models.TextField(null=True, blank=True)
    add_check = models.BooleanField(default=False)
    check = models.BooleanField(default=True)
    verify = models.BooleanField(default=True)
    member_chit_count = models.IntegerField(null=True,blank=True)
    added_members = models.BooleanField(default=True)


class Transactions(models.Model):
    member = models.TextField(null=True, blank=True)
    foreman = models.TextField(null=True, blank=True)
    chit = models.TextField(null=True, blank=True)
    transaction_id = models.TextField(null=True, blank=True)
    auction = models.TextField(null=True, blank=True)
    check = models.BooleanField(null=True, blank=True)
    trans_date = models.DateTimeField(null=True,blank=True)
    rtm_status = models.BooleanField(null=True,blank=True,default=False)
    paid_amount = models.TextField(null=True, blank=True,default=0)
    mem_count = models.IntegerField(null=True,blank=True)