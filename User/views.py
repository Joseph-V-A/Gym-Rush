from django.shortcuts import render

from django.urls import reverse
import datetime
from sqlite3 import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse, response
from .models import *
from Guest.models import *
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import FileResponse
from Gym.models import *


# Create your views here.


@csrf_exempt

def home(request):
    gmail=request.session['gmail']
    data={}
    if gmail!=None:
        ob= UserRegistration.objects.get(gmail=gmail)
        data["name"]=ob.name
    return render(request,"user/home.html",data)



@csrf_exempt
def profile(request):
    
    if request.POST:
        try:
            gmail=request.session['gmail']
            name=request.POST.get("Name")    
            Email=request.POST.get("Email") 
            Age=request.POST.get("Age") 
            Gender=request.POST.get("Gender") 
            ob=UserRegistration.objects.get(gmail=gmail)
            ob.name=name
            ob.age=Age
            ob.gender=Gender
            ob.gmail=Email
            ob.save()
            request.session['gmail']=Email


        except Exception as e:
            print(e)
    gmail=request.session['gmail']
    ob=UserRegistration.objects.get(gmail=gmail)
    ok = Book.objects.filter(cust=ob)
    print(ok)


    data1=[i for i in ok if i.status()==1]
    print(data1)
    return render(request,"user/profile.html",{"data":ob,"data1":data1[len(data1)-1] if len(data1)>0 else 0})



@csrf_exempt
def Gyms(request):
    try:
        if request.POST:            
            if request.POST.get("place")!="" and request.POST.get("gym")!="":
                ob=GymRegistration.objects.filter(place__iexact=request.POST.get("place"),gym_name__iexact=request.POST.get("gym"),status=1)
                data={"data":ob}
                data["place"]=request.POST.get("place")
                data["gym"]=request.POST.get("gym")
                return render(request,"user/searchgym.html",data)
            elif request.POST.get("place")!="":
                print("place")
                ob=GymRegistration.objects.filter(status=1,place__iexact=request.POST.get("place"))
                data={"data":ob}
                data["place"]=request.POST.get("place")
                return render(request,"user/searchgym.html",data)
            elif request.POST.get("gym")!="":
                print("gym")
                ob=GymRegistration.objects.filter(status=1,gym_name__iexact=request.POST.get("gym"))
                data={"data":ob}
                data["gym"]=request.POST.get("gym")
                return render(request,"user/searchgym.html",data)

    except Exception as e:
        print(e)
    ob=GymRegistration.objects.filter(status=1)



    data={"data":ob}
    print(ob)
    return render(request,"user/searchgym.html",data)






@csrf_exempt
def Gyms2(request,gym, **kwargs):
    print(kwargs)
    request.session['gym2']=kwargs.get("gym2")
    request.session['place']=kwargs.get("place")
    request.session['gym']=gym
    ob=GymRegistration.objects.get(gmail=gym)
    data={}
    data["name"]=ob.gym_name
    data["equ"]=ob.instruments.all
    data["rate"]=ob.month_rate
    data["rate1"]=ob.month_rate*12
    data["slot"]=Slot.objects.filter(Gym=ob)

    try:
        k=Ratings.objects.filter(gym=ob)
        data["r"]=k
    except Exception as e:
        pass
    

    return render(request,"user/Gyms2.html",data)
from datetime import date
from datetime import date, timedelta

@csrf_exempt
def Gym3(request):
    if request.POST.get("MONTLY")=="":
        gym=request.session['gym']
        ob=GymRegistration.objects.get(gmail=gym)
        data={"gym":ob}
        user=request.session['gmail']
        user=UserRegistration.objects.get(gmail=user)
        data["user"]=user
        data["date"] = date.today()
        #########  Compute Avalible seats
        total_Seats=Slot.objects.filter(Gym=ob)      
        summ=0
        for i in total_Seats:
            summ=summ+i.seats

        ava=Book.objects.filter(gym=ob)

        
        m=[1 for i in ava if i.status()==1]
        sum1=sum(m)

        if sum1<summ:
            billlist=["Monthly Plan",ob.month_rate,date.today() + timedelta(days=1),date.today() + timedelta(days=30)]
            data["billlist"]=billlist
            return render(request,"user/beforepay.html",data)
    if request.POST.get("YEARLY")=="":
        gym=request.session['gym']


        ob=GymRegistration.objects.get(gmail=gym)
        data={"gym":ob}
        user=request.session['gmail']
        user=UserRegistration.objects.get(gmail=user)
        data["user"]=user
        data["date"] = date.today()
        #########  Compute Avalible seats
        total_Seats=Slot.objects.filter(Gym=ob)      
        summ=0
        for i in total_Seats:
            summ=summ+i.seats

        ava=Book.objects.filter(gym=ob)

        
        m=[1 for i in ava if i.status()==1]
        sum1=sum(m)

        if sum1<summ:
            billlist=["Yearly Plan",ob.month_rate*12,date.today() + timedelta(days=1),date.today() + timedelta(days=366),total_Seats]
            data["billlist"]=billlist
            return render(request,"user/beforepay.html",data)
    
    if request.POST.get("type")=="Yearly" or request.POST.get("type")=="Monthly":
        print("dd")
        user=request.session['gmail']
        type=request.POST.get("type")
        gym=request.session['gym']
        if type=="Monthly":
            #### adding data to booking table

            Book.objects.create(cust=UserRegistration.objects.get(gmail=user),gym=GymRegistration.objects.get(gmail=gym),plan=1,Startdate=date.today() + timedelta(days=1),EndDate=date.today() + timedelta(days=31))


        elif type=="Yearly":
            slot=request.POST.get("type1")
            slot=Slot.objects.get(slotid=slot)
            Book.objects.create(cust=UserRegistration.objects.get(gmail=user),gym=GymRegistration.objects.get(gmail=gym),slot=slot,plan=2,Startdate=date.today() + timedelta(days=1),EndDate=date.today() + timedelta(days=366))
        return render(request,"user/payment.html")

    else:
        return redirect("User:Gyms")



@csrf_exempt
def back(request):
    val=request.session['gym2']
    val2=request.session['place']
    print(val,val2)
    if val2=="None":val2=None
    if val!=None and val2!=None:
        ob=GymRegistration.objects.filter(place__iexact=val2,gym_name__iexact=val,status=1)
        data={"data":ob}
        data["place"]=val2
        data["gym"]=val
        return render(request,"user/searchgym.html",data)
    if val!=None:
        ob=GymRegistration.objects.filter(gym_name__iexact=val,status=1)
        data={"data":ob}
        data["gym"]=val
        return render(request,"user/searchgym.html",data)
    if  val2!=None:
        ob=GymRegistration.objects.filter(place__iexact=val2,status=1)
        data={"data":ob}
        data["place"]=val2
        return render(request,"user/searchgym.html",data)
    else:
        ob=GymRegistration.objects.filter(status=1)
        data={"data":ob}
        return render(request,"user/searchgym.html",data)


@csrf_exempt
def my_workout_plain(request):
    user=request.session['gmail']
    ob=UserRegistration.objects.get(gmail=user)
    book = Book.objects.filter(cust=ob, EndDate__gte=datetime.now().date()).last()

    workout=Workoutplan.objects.filter(Bookid=book).order_by('-id')
    data={"data":workout}
    return render(request,"user/my_workout_plain.html",data)



from datetime import datetime, timedelta
@csrf_exempt
def slot(request):
    data={}
    user=request.session['gmail']
    ob=UserRegistration.objects.get(gmail=user)
    current_date = datetime.today().date()
    book = Book.objects.filter(cust=ob, EndDate__gte=datetime.now().date()).last()
    print(book)
    slt=SlotBooking.objects.filter(date=current_date +  timedelta(days=1),bookid=book).first()
    if book!=None and book.plan!=2 and slt==None:
        s=Slot.objects.filter(Gym=book.gym)
        data["slot"]=s
        data["date"]=current_date +  timedelta(days=1)
        data["sts"]=1
    elif book==None:
        data["sts"]=0 # not plan was choosed
    elif book.plan==2:
        data["sts"]=3 # your plan is yearly . so you are not eligible for this feacture
    elif slt!=None:
        data["sts"]=2 # your alredy selected the plan
        data["sts1"]=str(slt.Slotid.startTime)+" - "+str(slt.Slotid.endTime)
    if request.POST.get('time'):
        value=request.POST.get('time')
        print(value)
        if value!="000":
            SlotBooking.objects.create(date=current_date +  timedelta(days=1),bookid=book,Slotid=Slot.objects.get(slotid=value))
            return redirect("User:slot")
    return render(request,"user/slot.html",data)




@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        message = request.POST.get('msg')
        
        user_id=request.POST.get('user')
        print(user_id)
        user=request.session['gmail']
        ob=UserRegistration.objects.get(gmail=user)  
        Bookk=Book.objects.filter(cust=ob,EndDate__gte=datetime.now().date()).last()
        if user_id=='1':
            print("sending message to admin")
            Feedback.objects.create(msg=message,user=ob,reciver_sts=4,sender_sts=1)
        elif user_id=='2':
            print("sending message to gym")
            Feedback.objects.create(msg=message,user=ob,reciver_sts=3,sender_sts=1,Gym=Bookk.gym)
        return redirect("User:feedback")


    user=request.session['gmail']
    ob=UserRegistration.objects.get(gmail=user)
    Bookk=Book.objects.filter(cust=ob,EndDate__gte=datetime.now().date()).last()
    gym=0
    if Bookk!=None:
        gym=Bookk.gym.gym_name
    data={"gym":gym}
    feed=Feedback.objects.filter(user=ob)
    for i in feed:
        if i.reciver_sts==1:
            i.view_sts=1
            i.save()
    feed=Feedback.objects.filter(user=ob).order_by('-id')
    try:
        k=Book.objects.filter(cust=ob).last()
        data={"data":feed,"gym":k}
    except Exception as e:
        data={"data":feed}
    
    return render(request,"user/feedback.html",data)



@csrf_exempt
def feedback1(request):
    if request.method == 'POST':
        message = request.POST.get('msg1')
        star=request.POST.get('rate')
        user=request.session['gmail']
        ob=UserRegistration.objects.get(gmail=user)  
        k=Book.objects.filter(cust=ob).last()
        Ratings.objects.create(gym=k.gym,user=ob,star=star,comment=message)
        return redirect("User:feedback")
    else:
        return redirect("User:feedback")
