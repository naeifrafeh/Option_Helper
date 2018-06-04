# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import User,Job
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt
import datetime

def index(request):
    return render(request,'app/register.html')

def home(request):
    current_user = User.objects.get(id=request.session['userId'])
    print(current_user.firstname)
    user_jobs = Job.objects.filter(user = current_user) | Job.objects.filter(jobs = current_user)
    all_jobs = Job.objects.all()
    other_jobs = []
    for job in all_jobs:
        if not job in user_jobs:
            other_jobs.append(job)

    # User.objects.exclude(jobs = current_user).exclude(jobs = current_user)
    context={
        'jobs':user_jobs,
        'other_jobs':other_jobs,
        'current_user':current_user,
        'user_jobs':user_jobs
        
    }
    return render(request,'app/home.html',context)

def register(request):
	if request.method == "POST":
		User.objects.register(request)
		return redirect("/")
	else:
		return redirect("/")
def login(request):
	if User.objects.login(request):
		return redirect('/home')
	else:
		return redirect('/')

def add_job(request):
    if request.method == "POST":
        print ("inside Add Job")
        valid= Job.objects.jobvalidator(request)
       
        if valid:
            return redirect('/home')
        else: 
            print("trying to return ")
            return render(request,'app/add_job.html')
    else:
        return redirect('/add_job')

def add_to_myjob(request, id):
    try:
        job=Job.objects.get(id=id)
        print(job.title)
        current_user=User.objects.get(id=request.session['userId'])
        print(current_user.firstname)
        job.jobs.add(current_user)
        messages.info(request, 'users added')
        return redirect('/home')
    except:
        messages.info(request, 'add Not Found')
        return redirect('/home')
    context = {
        
        "job":job,
    }
    return render(request, 'app/detail.html', context)
   


def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    del request.session['id']
    return redirect('/')
def add_job_form(request):

    return render(request, 'app/add_job.html')
def show(request, id):
    try:
        job=Job.objects.get(id=id)
    except:
        messages.info(request, 'show Not Found')
        return redirect('/home')
    context = {
        
        "job":job,
    }
    return render(request, 'app/detail.html', context)

def remove(request,id):
    user = User.objects.get(id=request.session['userId'])
    job = Job.objects.get(id=id)
    Job.objects.get(id=id).delete()
    return redirect('/home')
def add(request,id):
    user = User.objects.get(id=request.session['userId'])
    job = Job.objects.get(id=id)
    user.jobs.add(job)
    return redirect('/home')

def edit_page(request,id):
    job = Job.objects.get(id=id)
    return render(request,'app/edit.html',{'job':job})



def edit(request,id):
    if request.method == "POST":
        job=Job.objects.get(id=id)
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.save()
       
    return redirect('/home')


