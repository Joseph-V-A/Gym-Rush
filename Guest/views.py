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
from Gym.models import *
from django.core.mail import send_mail
from django.urls.resolvers import settings
import random
# Create your views here.
def home(request):
    return render(request,'index.html')


def otp(request):
    gmail=request.session['gmail_otp']
    ob=UserRegistration.objects.filter(gmail=gmail).first()
    otp = random.randint(100000, 999999);
    otp=str(otp)
    subject = "Mail Verification"   
    message="""Hi, """+ob.name+"""                       
                            This is from Gym System.
    The OTP for Mail Verification is """+str(otp)+""" . Have a nice day. Thank you"""
    recipient = ob.gmail
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        print("send")
    except Exception as e:
        print(e)

    return render(request,'otp.html',{"otp":otp})


def forgotpassword(request):
    return render(request,'forgotpassword.html')    



def otp1(request):
    print("otp")
    gmail=request.session['gmail_otp']
    ob=UserRegistration.objects.filter(gmail=gmail).first()
    ob.status=1
    ob.save()         
    return render(request,'index.html')



def otp2(request):
    gmail=request.session['gmail_otp']
    ob=UserRegistration.objects.filter(gmail=gmail).first()
    ob.delete()   
    return render(request,'index.html')





def otpp(request):
    gmail=request.session['gmail_otp']
    ob=InstructorRegistration.objects.filter(gmail=gmail).first()
    otp = random.randint(100000, 999999);
    otp=str(otp)
    subject = "Mail Verification"   
    message="""Hi, """+ob.name+"""                       
                            This is from Gym System.
    The OTP for Mail Verification is """+str(otp)+""" . Have a nice day. Thank you"""
    recipient = ob.gmail
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        print("send")
    except Exception as e:
        print(e)

    return render(request,'otpp.html',{"otp":otp})


def otpp1(request):
    print("otp")
    gmail=request.session['gmail_otp']
    ob=InstructorRegistration.objects.filter(gmail=gmail).first()
    ob.status=1
    ob.save()         
    return render(request,'index.html')



def otpp2(request):
    gmail=request.session['gmail_otp']
    ob=InstructorRegistration.objects.filter(gmail=gmail).first()
    ob.delete()   
    return render(request,'index.html')



@csrf_exempt
def userreg(request):
    if request.method == 'POST':
        try:
            print(".................. USER REGISTRATION .....................")
            name=request.POST.get('name')
            age=request.POST.get('age')
            gmail=request.POST.get('gmail')
            password=request.POST.get('pass')
            gender=request.POST.get('gender')
            print(password)
            ob=UserRegistration.objects.create(name=name,age=age,gender=gender,gmail=gmail,password=password,status=0)
            request.session['gmail_otp']=ob.gmail
            print("success")
            data={"msg":"Successfully Registread"}
            return JsonResponse(data,safe=False)
        except IntegrityError:
            data={"msg":"Already exists"}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            data={"msg":"Failed"}
            return JsonResponse(data,safe=False)
    return render(request,'User.html')

@csrf_exempt
def gymreg(request):
    if request.method == 'POST':
        try:
            print(".................. GYM REGISTRATION .....................")
            gym_name = request.POST.get('gymname')
            place = request.POST.get('place').upper()
            owner_name = request.POST.get('name')
            instruments_ids = request.POST.get('instruments')  # Use getlist() for multiple values
            no_of_instructors = request.POST.get('empoy')
            gmail = request.POST.get('gmail')
            password = request.POST.get('pass')
            # Create GymRegistration instance
            ob = GymRegistration.objects.create(
                gym_name=gym_name,
                place=place,
                owner_name=owner_name,
                no_of_instructors=no_of_instructors,
                gmail=gmail,
                password=password,
                status=0
            )
        
            # Add instruments to the GymRegistration instance
            try:
                for instrument_id in instruments_ids:
                    print(instrument_id)
                    equipment = Equipment.objects.get(id=instrument_id)
                    ob.instruments.add(equipment)
            except Exception as e:
                print(e)
            return JsonResponse({"msg": "Registration Done"}, safe=False)
        except IntegrityError:
            data = {"msg": "Already exists"}
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)
            data = {"msg": "Failed"}
            return JsonResponse(data, safe=False)
    return render(request, 'Owner.html')

@csrf_exempt
def gymreg2(request):
    print("request")
    ok=Equipment.objects.all()
    dict={"inst":ok}
    return render(request,'Owner2.html',dict)


@csrf_exempt

def instreg(request):
    if request.method == 'POST':
        try:
            print(".................. Instructor REGISTRATION .....................")
            name=request.POST.get('name')
            age=request.POST.get('age')
            gmail=request.POST.get('gmail')
            password=request.POST.get('pass')
            gender=request.POST.get('gender')
            cv_docs=request.POST.get("proof")
            cv_docs=request.FILES['proof']


            #current_gym=request.GET.get("current_gym")
            ob=InstructorRegistration.objects.create(name=name,gender=gender,gmail=gmail,password=password,cv_and_documents=cv_docs,status=0)
            data={"msg":"Successfully Registread"}
            request.session['gmail_otp']=ob.gmail
            return JsonResponse(data,safe=False)

        except IntegrityError:
            data={"msg":"Already exists"}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            data={"msg":"Failed"}
            return JsonResponse(data,safe=False)

    return render(request,'trainer.html')

@csrf_exempt
def login(request):


    if request.method == 'POST':
        print("------ Login Request Processing -------")
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        type=request.POST.get('type')
        print(request.POST)
        try:
            if userid=="admin" and password=="admin" and type=="ADMIN":
                return JsonResponse({'status': 1})
            elif type=="GYM":
                ob=GymRegistration.objects.get(gmail=userid,password=password,status=1)
                request.session['gmail']=ob.gmail
                return JsonResponse({'status': 2})
            elif type=="INSTRUCTOR":
                ob=InstructorRegistration.objects.get(gmail=userid,password=password,status=1)
                request.session['gmail']=ob.gmail
                return JsonResponse({'status': 3})
            else:
                ob=UserRegistration.objects.get(gmail=userid,password=password,status=1)
                request.session['gmail']=ob.gmail
                return JsonResponse({'status': 4})
        except Exception as e:
            print(e)
            return JsonResponse({'status': "failed"})
    return render(request,'Login.html')

@csrf_exempt
def viewgyms(request):
    try:
        if request.POST:            
            if request.POST.get("place")!="" and request.POST.get("gym")!="":
                ob=GymRegistration.objects.filter(place__iexact=request.POST.get("place"),gym_name__iexact=request.POST.get("gym"),status=1)
                data={"data":ob}
                data["place"]=request.POST.get("place")
                data["gym"]=request.POST.get("gym")
                return render(request,"searchgym.html",data)
            elif request.POST.get("place")!="":
                print("place")
                ob=GymRegistration.objects.filter(status=1,place__iexact=request.POST.get("place"))
                data={"data":ob}
                data["place"]=request.POST.get("place")
                return render(request,"searchgym.html",data)
            elif request.POST.get("gym")!="":
                print("gym")
                ob=GymRegistration.objects.filter(status=1,gym_name__iexact=request.POST.get("gym"))
                data={"data":ob}
                data["gym"]=request.POST.get("gym")
                return render(request,"searchgym.html",data)

    except Exception as e:
        print(e)
    ob=GymRegistration.objects.filter(status=1)
    data={"data":ob}
    print(ob)
    return render(request,"searchgym.html",data)



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
    return render(request,"Gyms2.html",data)





@csrf_exempt
def forgotpassword1(request):
    print("jjjj")
    if request.method == 'POST':
        print("------ Password Request Processing -------")
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        type=request.POST.get('type')
        print(request.POST)
        try:
            if userid=="admin" and password=="admin" and type=="ADMIN":
                return JsonResponse({'status': 0})
            elif type=="GYM":
                ob=GymRegistration.objects.get(gmail=userid,status=1)
                gmailid=ob.gmail

                otp = random.randint(100000, 999999);
                otp=str(otp)
                subject = "Password Change"   
                message="""Hi, """+ob.gym_name+"""                       
                                        This is from Gym System.
                The OTP for Change password is """+str(otp)+""" . Have a nice day. Thank you"""
                recipient = gmailid
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                    print("send")
                except Exception as e:
                    print(e)






                return JsonResponse({'status': 1,'otp':otp})
            elif type=="INSTRUCTOR":
                ob=InstructorRegistration.objects.get(gmail=userid,status=1)
                gmailid=ob.gmail
                otp = random.randint(100000, 999999);
                otp=str(otp)
                subject = "Password Change"   
                message="""Hi, """+ob.name+"""                       
                                        This is from Gym System.
                The OTP for Change password is """+str(otp)+""" . Have a nice day. Thank you"""
                recipient = gmailid
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                    print("send")
                except Exception as e:
                    print(e)



                return JsonResponse({'status': 1,'otp':otp})
            else:
                ob=UserRegistration.objects.get(gmail=userid,status=1)
                gmailid=ob.gmail


                otp = random.randint(100000, 999999);
                otp=str(otp)
                subject = "Password Change"   
                message="""Hi, """+ob.name+"""                       
                                        This is from Gym System.
                The OTP for Change password is """+str(otp)+""" . Have a nice day. Thank you"""
                recipient = gmailid
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                    print("send")
                except Exception as e:
                    print(e)


                return JsonResponse({'status': 1,'otp':otp})
        except Exception as e:
            print(e)
            return JsonResponse({'status': "failed"})
    return JsonResponse({'status': "failed"})





@csrf_exempt
def forgotpassword2(request):
    if request.method == 'POST':
        print("------ Password Request Processing -------")
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        type=request.POST.get('type')
        print(request.POST)
        try:
            if userid=="admin" and password=="admin" and type=="ADMIN":
                return JsonResponse({'status': 0})
            elif type=="GYM":
                ob=GymRegistration.objects.get(gmail=userid,status=1)
                ob.password=password
                ob.save()
                return JsonResponse({'status': 1})
            elif type=="INSTRUCTOR":
                ob=InstructorRegistration.objects.get(gmail=userid,status=1)
                ob.password=password
                ob.save()
                return JsonResponse({'status': 1})
            else:
                ob=UserRegistration.objects.get(gmail=userid,status=1)
                ob.password=password
                ob.save()
                return JsonResponse({'status': 1})
        except Exception as e:
            print(e)
            return JsonResponse({'status': "failed"})
    return JsonResponse({'status': "failed"})
    