from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt
from datetime import date, datetime
from time import strptime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
password_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def register(self,request):
        if len(request.POST['firstname']) < 1 :
             messages.add_message(request,messages.ERROR, 'this is invalid firstname ')
        if len(request.POST['lastname']) < 1 :
             messages.add_message(request,messages.ERROR, 'this is invalid last name ')
        if len(request.POST['email']) < 1:
            messages.add_message(request,messages.ERROR, 'email can not be empty ')
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.add_message(request,messages.ERROR, 'email must match format ')
        if len(request.POST['password'])< 8:
            messages.add_message(request,messages.ERROR, 'passwprd must be between 8 to 32  ')
        if not password_REGEX.match(request.POST['password']):
            messages.add_message(request,messages.ERROR, 'password must match format ')
        if request.POST['password'] != request.POST['password_confirm'] :
            messages.add_message(request,messages.ERROR, 'password much match confirm password  ')
        if User.objects.filter(email=request.POST['email']).count() >0:
            messages.add_message(request,messages.ERROR, 'user with this email is already exist')
        if len(get_messages(request)) >0:
            return False
        else:
            User.objects.create(
                firstname=request.POST['firstname'],
                lastname=request.POST['lastname'],
                email=request.POST['email'],

                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            )
            return True
    def login(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            # user.save()
          
            # request.session['userId'] = user.id

            isvalid = bcrypt.hashpw(request.POST['password'].encode(), user.password.encode())
            print('*'*100)
            if isvalid:
                request.session['userId']= user.id
                return True
            else :
                messages.add_message(request,messages.ERROR, "Invalid Credunthial")
                return False


        except:
             messages.add_message(request,messages.ERROR, 'user does not exist')
             return False

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # friends = models.ManyToManyField('User', related_name="users_friended")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class JobManager(models.Manager):
    def jobvalidator(self,request):
        user = User.objects.get(id = request.session['userId'])
        if len(request.POST['title']) < 3 :
             messages.add_message(request,messages.ERROR, 'this is invalid title ')
        if len(request.POST['description']) < 10 :
             messages.add_message(request,messages.ERROR, 'this is invalid description ')
        if len(request.POST['location']) < 1:
            messages.add_message(request,messages.ERROR, 'location can not be empty ')
        if len(get_messages(request)) >0:
            print("return false")
            return False

        else:
            Job.objects.create(
                title=request.POST['title'],
                location=request.POST['location'],
                description=request.POST['description'],
                user=user
            )
            return True

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    jobs =models.ManyToManyField(User, related_name="users_jobs")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="jobs")
    
    objects = JobManager()




