from rest_framework.response import Response
from rest_framework import status
import random
from django.contrib.auth.models import User
# from urllib2 import Request, urlopen
# from urllib import urlencode
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.decorators import api_view
import hashlib
from Administration.models import RolePermissionFeature
import json
import jwt
from urllib.parse import urlencode
from urllib.request import Request,urlopen




def generate_otp(request):
    print("generate",request.data)
    mobile_number = request.data['username']
    otp = get_otp()
    print("ottttttttt",otp)
    user = User.objects.filter(username=mobile_number)
    print("new useeeeeeeeee",user)
    if user:
        print("innnnnnnnnn",user.values())
        return ("Already registered")
    else:
        print("elllllllll")
        sendSMS(otp, mobile_number)
        return otp

def get_otp():
    otp = random.randrange(100000, 999999)
    user = User.objects.filter(last_name=otp)
    if user:
        print("inside GETOTPOPPPPPPPPPPPPPPPPPPP")
        get_otp()
    return otp



def sendSMS(otp, mobilenumber):
    url = 'http://api.textlocal.in/send/?'
    msg = 'Thank you for registering with GFUNDS. Please enter the verification code ' + str(otp) + \
                      ' to complete the registration.'
    post_fields = urlencode({"username": "devaraj.gowdanar@gmail.com",
                                         "hash": "c2356d73cdce10638457ed4d4e222adcb22d9aea56e48e475de28280ac4678b1", "numbers": mobilenumber,
                                         "message": msg, 'sender': 'GFUNDS'})
    post_fields = post_fields.encode('utf-8')
    request = Request(url)
    json = urlopen(request, data=post_fields)
    print("otppppppppppppppp", json)
    f = json.read()
    print("mmmmmmmmmmmmmmmmmmmmmmmmmmm", f)



def authentication(token):
    try:
        print("sacccccccccccccc",token)
        payload = jwt.decode(token, "SECRET_KEY")
        userid = payload['id']
        msg = {'Error': "Token mismatch", 'status': "401"}
        user = User.objects.get(id=userid,is_active=True)
        if not user:
            print("user does not exist")
        print("userrrrrrr",user.id)
        return user.id

    except Exception as e:
        print("hi1111111111111111", e)

@api_view(['POST'])
def verify_otp(request):
    print("reeeeeeeeeeeeeeeee",request.data)
    otp_fe = request.data['otp']
    try:
        otp_db = User.objects.filter(username = request.data['username'],last_name=otp_fe)
        print("hhhhhhhhh",otp_db)
        if otp_db:
            otp_db[0].last_name = ""
            otp_db[0].save()
            return Response("OTP verified", status=status.HTTP_200_OK)
        else:
            return Response("Invalid OTP")
    except Exception as e:
        print("VERify",e)
        return Response("Invalid OTP",status=status.HTTP_400_BAD_REQUEST)


def encrypt_password(password):
    encrypt = hashlib.md5(password.encode('utf-8')).hexdigest()
    return encrypt

def get_features(role, id1):
    feature = []
    role = RolePermissionFeature.objects.filter(role=role, profile=id1)
    print(role)
    for role1 in role:
        feature.append(role1.feature)
    return set(feature)

@api_view(['POST'])
def forgot_password(request):
    mobile = request.data['username']
    try:
        user = User.objects.get(username=mobile)
        if user:
            otp = get_otp()
            # sendSMS(otp,mobile)
            user.last_name = otp
            user.save()
            return Response(otp)
    except Exception as e:
        return Response("Mobile Number doesnt exist")
        print(e)

@api_view(['POST'])
def reset_password(request):
    print("eeeeeee",request.data)
    try:
        password = request.data['confirmpassword']
        username = request.data['username']
        encrypt = encrypt_password(password)
        user = User.objects.get(username=username)
        print("gg",user)
        if user:
            user.password = encrypt
            user.save()
            return Response('password changed successfully')
    except Exception as e:
        print(e)


def authUserId():
    count = User.objects.all().count()
    return count + 1




































