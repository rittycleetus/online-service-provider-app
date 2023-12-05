from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
   
    user_type = models.CharField(default=1, max_length=10)

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    ph=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='image/', blank=True)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='image/', blank=True)
    availability = models.BooleanField(default=True)



class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    rating = models.IntegerField()
    comment = models.TextField()

class WorkerProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255,null=True)
    agency_name = models.CharField(max_length=255, blank=True,null=True)
    phone=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='image/',blank=True,null=True)
    workexp=models.IntegerField(null=True)
    dob=models.DateField(auto_now_add=False,auto_now=False,blank=True,null=True)
    typeofid=models.CharField(max_length=255,null=True)
    idproof=models.FileField(upload_to='file/',null=True)


    
class WorkerProfile1(models.Model):
    first_name=models.CharField(max_length=255,null=True)
    last_name=models.CharField(max_length=255,null=True)
    username=models.CharField(max_length=255,null=True)
    email=models.CharField(max_length=255,null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255,null=True)
    agency_name = models.CharField(max_length=255, blank=True,null=True)
    phone=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='image/',null=True)
    workexp=models.IntegerField(null=True)
    dob=models.DateField(auto_now_add=False,auto_now=False,blank=True,null=True)
    typeofid=models.CharField(max_length=255,null=True)
    idproof=models.FileField(upload_to='file/',null=True)
    def get_file_type(self):
        # Get the file extension
        file_extension = self.idproof.name.split('.')[-1].lower()
        return file_extension
    

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=255,null=True)
    is_approved = models.BooleanField(default=False)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,null=True)
    is_completed=models.BooleanField(default=False)
    worker=models.ForeignKey(WorkerProfile,on_delete=models.CASCADE,null=True)

class Notification(models.Model):
    sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    message=models.TextField()
    is_read=models.BooleanField(default=False)

    



    
    



