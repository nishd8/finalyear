from django.db import models
import uuid

# Create your models here.
class Account(models.Model):
    acc_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100, blank=False)
    dob = models.DateField(blank=False)
    father = models.CharField(max_length=100, blank=True)
    aadhar = models.CharField(max_length=12,blank=False,unique=True)
    pan = models.CharField(max_length=10,blank=False,unique=True)
    phone=models.CharField(max_length=10,blank=False,unique=True)
    status = models.BooleanField(default=False)



class Otp(models.Model):
    opt_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    otp=models.CharField(max_length=6,blank=False)
    phone=models.CharField(max_length=10,blank=False,unique=True)

class Transaction(models.Model):
    transaction_id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE,blank=False, null=False,related_name='sender')
    reciever = models.ForeignKey(Account,on_delete=models.CASCADE,blank=False, null=False,related_name='reciever')
    time_stamp = models.DateTimeField(auto_now_add=True)
    amount=models.FloatField(default=0)

class Balance(models.Model):
    b_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    account_id= models.ForeignKey(Account, on_delete=models.CASCADE,blank=False, null=False)
    balance = models.FloatField(blank=False,default=0,)


class Admin(models.Model):
    acc_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100, blank=False)
    dob = models.DateField(blank=False)
    phone=models.CharField(max_length=10,blank=False,unique=True)
    password=models.CharField(max_length=50,blank=False)