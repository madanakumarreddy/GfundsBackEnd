from rest_framework import serializers

from Foreman.models import ForemanProfile


class ForemanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForemanProfile
        exclude = ['id','user','full_name','mobile_number','date_of_birth','role']


class EditForeman(serializers.ModelSerializer):
    class Meta:
        model = ForemanProfile
        exclude = ['id','user','mobile_number','date_of_birth','role','address_proof','bank_statement','employee_id_card','certificate_of_registration',
                   'business_bank_statement','company_pancard','company_address_proof','aggrement','front_photo','chit_company_logo','chit_company_licence']
