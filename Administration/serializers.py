from rest_framework import serializers


from Foreman.models import Chits,ForemanProfile
from Members.models import MemberProfile


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chits
        exclude = ['fixeddepositcopy','govtissuedcopy','company_logo','amount_in_string','duration_in_string']

class ForemanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForemanProfile
        exclude=['user', 'gender','address_proof', 'bank_statement', 'employee_id_card', 'certificate_of_registration', 'chit_company_logo', 'business_bank_statement', 'company_pancard', 'company_address_proof', 'aggrement', 'front_photo', 'chit_company_licence']



class EditAppMembers(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        exclude = ['present_address_proof','aadharimage','user','pay_slip2','pay_slip3','bank_statement','pay_slip1','employe_id_card','addagrementcopy','rtmagrementcopy',
                   'agrementcopy','cibil_score_file','business_adressproof','front_photo','panimage','itreturn','incometaxpayer']