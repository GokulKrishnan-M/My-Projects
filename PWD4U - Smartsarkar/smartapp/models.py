from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Public(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    phone=models.BigIntegerField()
    aanum = models.CharField(max_length=100,null=True)
    email=models.EmailField()
    regdate=models.DateField(auto_now_add=True)
    image = models.ImageField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Authority(models.Model):
    authorityname=models.CharField(max_length=100)
    official=models.CharField(max_length=100)
    offdesig = models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=500)
    dist = models.CharField(max_length=100,null=True)
    phone=models.BigIntegerField()
    email=models.EmailField()
    proof=models.ImageField()
    regdate = models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Complaint(models.Model):
    pid=models.ForeignKey(Public,on_delete=models.CASCADE,null=True)
    aid=models.ForeignKey(Authority,on_delete=models.CASCADE,null=True)
    complaint=models.CharField(max_length=500,null=True)
    desc=models.CharField(max_length=500,null=True)
    proof=models.ImageField(null=True)
    status=models.CharField(max_length=100,null=True)
    rply=models.CharField(max_length=500,null=True)
    date=models.DateField(auto_now_add=True)
    lon = models.CharField(max_length=50,null=True)
    lat = models.CharField(max_length=50,null=True)
    authority=models.CharField(max_length=50,null=True)
    aldt=models.DateField(auto_now_add=True,null=True)
    duedt=models.DateField(null=True)
    addinfo=models.CharField(max_length=50,null=True)



class Feedback(models.Model):
    pid=models.ForeignKey(Public,on_delete=models.CASCADE,null=True)
    Feedback=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)


    
class Allocation(models.Model):
    compid=models.ForeignKey(Complaint,on_delete=models.CASCADE,null=True)
    authid=models.ForeignKey(Authority,on_delete=models.CASCADE,null=True)

class Rating(models.Model):
    pid=models.ForeignKey(Public,on_delete=models.CASCADE,null=True)
    aid=models.ForeignKey(Authority,on_delete=models.CASCADE,null=True)
    rating=models.BigIntegerField(null=True)

