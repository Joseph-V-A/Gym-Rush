import datetime
from sqlite3 import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, response
from .models import *
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import FileResponse
from Guest.models import UserRegistration,InstructorRegistration,GymRegistration,Feedback


# Create your views here.

@csrf_exempt

def home(request):
    return render(request,'admin/home.html')



@csrf_exempt

def view_gym(request):
    #or operation using q import
    ob=GymRegistration.objects.filter(Q(status=2) | Q(status=1))
    data={}
    data["data"]=ob
    return render(request,'admin/view_gym.html',data)


@csrf_exempt

def view_gym2(request):
    gym=request.GET.get("btn1")

    if request.POST.get("block"):
        print(" block")
        gym=request.POST.get("block")
        ob=GymRegistration.objects.get(gmail=gym)
        ob.status=2
        ob.save()
    if request.POST.get("unblock"):
        print("un block")
        gym=request.POST.get("unblock")
        ob=GymRegistration.objects.get(gmail=gym)
        ob.status=1
        ob.save()
    data={}
    ob=GymRegistration.objects.get(gmail=gym)
    data["gym"]=ob
    data["inst"]=[{"name":"jihin","id":"jithin123"},{"name":"jihin","id":"jithin123"}]
    return render(request,'admin/view_gym2.html',data)    




@csrf_exempt

def view_instructor(request):
    if request.POST.get("block"):
        gmail=request.POST.get("block")
        ob=InstructorRegistration.objects.get(gmail=gmail)
        ob.status=0
        ob.save()        
    if request.POST.get("unblock"):
        gmail=request.POST.get("unblock")
        ob=InstructorRegistration.objects.get(gmail=gmail)
        ob.status=1
        ob.save()
    ob=InstructorRegistration.objects.filter()
    data={}
    data["data"]=ob 
    return render(request,'admin/view_instructor.html',data)



@csrf_exempt

def view_user(request):
    if request.POST.get("block"):
        gmail=request.POST.get("block")
        ob=UserRegistration.objects.get(gmail=gmail)
        ob.status=0
        ob.save()        
    if request.POST.get("unblock"):
        gmail=request.POST.get("unblock")
        ob=UserRegistration.objects.get(gmail=gmail)
        ob.status=1
        ob.save()
    ob=UserRegistration.objects.all()
    data={}
    data["data"]=ob 
    return render(request,'admin/view_users.html',data)



@csrf_exempt

def view_request(request):
    if request.POST.get("reject"):
        gmail=request.POST.get("reject")
        ob=GymRegistration.objects.get(gmail=gmail)
        ob.delete()   
    if request.POST.get("approve"):
        gmail=request.POST.get("approve")
        ob=GymRegistration.objects.get(gmail=gmail)
        ob.status=1
        ob.save()
    ob=GymRegistration.objects.filter(status=0)
    data={}
    data["gym"]=ob     
    return render(request,'admin/view_request.html',data)




@csrf_exempt

def instruments(request):

    if request.POST:
        image = request.FILES.get("image")
        id=request.POST.get("id")
        delete=request.POST.get("delete")
        name=request.POST.get("equipmentName")
        print("img=",image,"id=",id,"delete=",delete,"name=",name)
        if id!=None:
            name=request.POST.get("equipmentName")
            description=request.POST.get("description")

            ob=Equipment.objects.get(id=id)
            print(image)
            if image!=None:
                ob.Image=image
            ob.Description=description
            ob.Name=name
            ob.save()

        elif delete!=None:
            ob=Equipment.objects.get(id=delete)
            ob.delete()
        elif name!=None:
            name=request.POST.get("equipmentName")
            description=request.POST.get("description")
            image=request.FILES.get("image")
            Equipment.objects.create(Name=name,Description=description,Image=image)
        else:
            pass             
                
    ob=Equipment.objects.all()
    data={}
    data["data"]=ob
    return render(request,'admin/instruments.html',data)

from django.db.models import Q


@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('msg')
            user_name=request.POST.get('user_id')
            user_id=request.POST.get('user')
            print(user_id)
            
            if user_id=='1':
                JJ=GymRegistration.objects.get(gmail=user_name)
                print("sending message to gym")
                Feedback.objects.create(msg=message,Gym=JJ,reciver_sts=3,sender_sts=4)
            elif user_id=='2':
                JJ=InstructorRegistration.objects.get(gmail=user_name)
                print("sending message to instructor")
                Feedback.objects.create(msg=message,instructor=JJ,reciver_sts=2,sender_sts=4)
            elif user_id=='3':
                JJ=UserRegistration.objects.get(gmail=user_name)
                print("sending message to member")
                Feedback.objects.create(msg=message,user=JJ,reciver_sts=1,sender_sts=4)
            return redirect("Admin:feedback")
        except Exception as e:
            return redirect("Admin:feedback")



    feed=Feedback.objects.filter(reciver_sts=4)
    for i in feed:
        if i.reciver_sts==4:
            i.view_sts=1
            i.save()
    feed = Feedback.objects.filter(Q(reciver_sts=4) | Q(sender_sts=4)).order_by('-id')

    data={"data":feed}
    return render(request,"admin/feedback.html",data)


