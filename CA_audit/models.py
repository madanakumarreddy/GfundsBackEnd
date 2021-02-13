from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class CaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.TextField(null=True ,default="ca")
    email_id = models.EmailField(max_length=150, )
    mobile_number = models.TextField(null=True, unique=True)
    password = models.TextField()
