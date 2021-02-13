from rest_framework import serializers

from Foreman.models import FinalAuctions
from .models import MemberProfile


class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        exclude = ['user', 'id', 'role', 'full_name', 'date_of_birth', 'mobile_number','front_photo']


class MemberEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        exclude = ['id','user','role','front_photo','present_address_proof','employe_id_card','pay_slip1','pay_slip2','pay_slip3','cibil_score_file',
                   'bank_statement','panimage','aadharimage','agrementcopy','addagrementcopy','rtmagrementcopy','business_adressproof',
                   'itreturn']

class MemberDashboardViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['full_name',
                  'front_photo',
                  'gchits_score',
                  'id',
                  'member_rating'
                  ]
class FinalAuctionsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalAuctions
        fields = '__all__'