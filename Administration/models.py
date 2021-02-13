# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from Foreman.models import ForemanProfile


class ExecutiveProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.TextField(null=True)
    email_id = models.EmailField(max_length=150, unique=True)
    mobile_number = models.TextField(null=True, unique=True)
    password = models.TextField()

    def __str__(self):
        return str(self.id)

class RolePermissionFeature(models.Model):
    role = models.CharField(max_length=30, null=True, blank=True)
    name = models.TextField(max_length=20, null=True, blank=True)
    profile = models.TextField(max_length=20, null=True, blank=True)
    feature = models.CharField(max_length=20, null=True, blank=True)
    permission = models.CharField(max_length=20, null=True, blank=True)
    sub_feature = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.feature)

class Role(models.Model):
    role = models.TextField(unique=True, null=True, blank=True)




class Resellers_Referel(models.Model):
    reseller_id = models.ForeignKey(ExecutiveProfile,on_delete=models.CASCADE)
    reseller_name = models.CharField(max_length=100, null=True, blank=True)
    foreman_id = models.ForeignKey(ForemanProfile,on_delete=models.CASCADE)
    foreman_name = models.CharField(max_length=100, null=True, blank=True)