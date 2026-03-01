from django.shortcuts import render,redirect
from Guest.views import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.db.models import Q


@csrf_exempt

def home(request):
    gmail=request.session['gmail']
    data={}
    if gmail!=None:
        ob=GymRegistration.objects.get(gmail=gmail)
        data["name"]=ob.gym_name
    return render(request,"gym/home.html",data)


@csrf_exempt
def profile(request):
    gmail=request.session['gmail']
    ob=GymRegistration.objects.get(gmail=gmail) 
    data={}
    if request.POST:
        ob.month_rate=request.POST.get("rate")
        ob.gym_name=request.POST.get("gym_name")
        ob.place=request.POST.get("place")
        ob.gmail=request.POST.get("gmail")
        lis=request.POST.getlist("instruments")
        for i in lis:
            oi=Equipment.objects.get(id=i)
            ob.instruments.add(oi)
        ob.no_of_instructors=request.POST.get("no_of_instructors")
        ob.save()
        request.session['gmail']=ob.gmail
    gmail=request.session['gmail']

    ob=GymRegistration.objects.get(gmail=gmail) 
    data["data"]=ob
    ob2=Equipment.objects.all()
    data["innst"]=ob2

    return render(request,"gym/profile.html",data)


from datetime import datetime

@csrf_exempt
def attendence(request):
    gmail=request.session['gmail']
    data={}

    
    if request.POST.get("date"):
        print("REKLFJKLDSJFDSJFSDJF")
        date=request.POST.get("date")
        print(date)
        date_str = date  # Define the date string
        date = datetime.strptime(date_str, '%Y-%m-%d')  # Parse the date string into a datetime object
        
        if datetime.now() >= date:
            ob1=GymRegistration.objects.get(gmail=gmail)
            ob=Job.objects.filter(employer=ob1,staus=1)
            datalist=[]
            for i in ob:
                data1={
                "employeeid":i.employe.gmail,
                "name":i.employe.name,
                "status": 1 if Attendance.objects.filter(Gym=ob1, trainer=InstructorRegistration.objects.get(gmail=i.employe.gmail), date=date).exists() else 0
                }
                datalist.append(data1)
            data["data"]=datalist
            print("SD")
            print(data)


            return JsonResponse(data,safe=False)
    if request.method == "POST" and request.POST.get("employee_id"):
        date = request.POST.get("date1")
        employee_id = request.POST.get("employee_id")
        status = request.POST.get("status")

        ob = GymRegistration.objects.get(gmail=gmail)

        try:
            print("hiiiiiii")
            # Try to get the existing Attendance object
            attendance_obj = Attendance.objects.get(Gym=ob, trainer=InstructorRegistration.objects.get(gmail=employee_id), date=date)
            attendance_obj.status = status
            attendance_obj.save()
        except Exception as e:
            
            Attendance.objects.create(Gym=ob, trainer=InstructorRegistration.objects.get(gmail=employee_id), date=date, status=status)

        return JsonResponse({"message": "Data saved successfully."})
    if request.method == "POST" and request.POST.get("approve"):
        id=request.POST.get("approve_id")
        status=request.POST.get("approve")
        ob=Leave.objects.get(id=id)
        ob.status=status
        ob.save()
    objj=Leave.objects.filter(to=GymRegistration.objects.get(gmail=gmail),status=0)
    data["leave"]=objj
    return render(request,"gym/attendence.html",data)





@csrf_exempt
def attendence2(request):
    gmail=request.session['gmail']
    data={}

    print("new one")
    if request.POST.get("date"):
        date=request.POST.get("date")
        print(date)
        date_str = date  # Define the date string
        date = datetime.strptime(date_str, '%Y-%m-%d')  # Parse the date string into a datetime object
        data={}
        if datetime.now() >= date:
            ob1=GymRegistration.objects.get(gmail=gmail)
            ob=Book.objects.filter(gym=ob1,Startdate__lte=date, EndDate__gte=date)
            
            datalist=[]
            for i in ob:
                k=SlotBooking.objects.filter(date=date,bookid=i).first()
                if i.status()==0:
                    print(i)
                    continue
                data1={
                "employeeid":i.cust.gmail,
                "name":i.cust.name,
                "status":"Not Marked" if k==None else 1 if k.status==1 else 0 if k.status==0 else ""
                }
                datalist.append(data1)
            data["data"]=datalist
            print("SD")
            print(data)


            return JsonResponse(data,safe=False)
        return JsonResponse(data,safe=False)









@csrf_exempt
def remove_trainer(request,gmail):
    gmail1=request.session['gmail']
    print(" removing from job ",gmail)
    ob=InstructorRegistration.objects.get(gmail=gmail)
    ob2=GymRegistration.objects.get(gmail=gmail1)
    obj=Job.objects.get(employer=gmail1,employe=gmail)
    if obj.staus==0:
        obj.delete()
    else:
        obj.staus=2
        obj.save()
    return redirect("gym:instructor")


@csrf_exempt
def instructor(request):
    gmail=request.session['gmail']
    ob=GymRegistration.objects.get(gmail=gmail) 
    data={}
    total=ob.no_of_instructors-1
    incr=0
    ob1 = Job.objects.filter(employer=gmail).filter(Q(staus=1) | Q(staus=0))
    print(ob1)
    list=[]
     
    for i in ob1:
        print(i)
        
        if incr<=total:
            datalis={
                "number":incr,
                "value":i
            }
            list.append(datalis)
        incr=incr+1
    for i in range(incr,total+1):
        datalis={
                "number":i,
                "value":None            
        }
        list.append(datalis)
    
    data["data"]=list
    print(list)
    on=JobApplication.objects.filter(gym=ob,status=0)
    data["applications"]=on
    return render(request,"gym/instructor.html",data)


@csrf_exempt
def ApplicationAccept(request,id):
    on=JobApplication.objects.filter(id=id).first()
    return render(request,"gym/jobapplication.html",{"on":on})



@csrf_exempt
def ApplicationAccept1(request):
    try:
        id=request.POST.get("id")
        cmd=request.POST.get("comment")
        sal=request.POST.get("salary")
        on=JobApplication.objects.filter(id=id).first()
        on.status=1
        on.comment=cmd
        on.save()
        Job.objects.create(employe=on.instructor,employer=on.gym,salary=sal,staus=0)
    except Exception as e:
        pass
    return redirect("gym:instructor")




@csrf_exempt
def ApplicationReject1(request):
    try:
        id=request.POST.get("id")
        cmd=request.POST.get("reason")
        on=JobApplication.objects.filter(id=id).first()
        on.status=2
        on.comment=cmd
        on.save()
    except Exception as e:
        pass
    return redirect("gym:instructor")





@csrf_exempt
def CheckUsers(request):
    data = {}
    ob = None
    try:
        ob = InstructorRegistration.objects.get(gmail=request.POST.get("userid"))
    except InstructorRegistration.DoesNotExist:
        pass  # Handle the case where the object is not found
    if ob:
        serialized_data = serializers.serialize('json', [ob])
        data['data'] =serialized_data
    else:
        data['data'] = None 
    print("sjjjjjj")
    return JsonResponse(data, safe=False)



@csrf_exempt
def sendoffer(request):
    gmail2=request.session['gmail']
    gmail=request.POST.get("gmail")
    salary=request.POST.get("salary")
    print(salary)
    if salary==None:salary=0
    try:
        salary=int(salary)
        print(gmail)
        ob=InstructorRegistration.objects.get(gmail=gmail)
        ob1=GymRegistration.objects.get(gmail=gmail2)
        Job.objects.create(employe=ob,employer=ob1,salary=salary,staus=0)
        return redirect('gym:instructor')
    except Exception as e:
        print(e)
        return redirect('gym:instructor')


@csrf_exempt
def members(request):
    gmail=request.session['gmail']
    monthlyyearly=Book.objects.filter(gym=GymRegistration.objects.get(gmail=gmail),EndDate__gte=datetime.now().date())
    monthly=Book.objects.filter(gym=GymRegistration.objects.get(gmail=gmail),EndDate__gte=datetime.now().date(),plan=1)
    monthlyExp=Book.objects.filter(gym=GymRegistration.objects.get(gmail=gmail),EndDate__lt=datetime.now().date(),plan=1)
    Yearly=Book.objects.filter(gym=GymRegistration.objects.get(gmail=gmail),EndDate__gte=datetime.now().date(),plan=2)
    YearlyExp=Book.objects.filter(gym=GymRegistration.objects.get(gmail=gmail),EndDate__lt=datetime.now().date(),plan=2)
    data={"monthly":monthly,"monthlyExp":monthlyExp,"Yearly":Yearly,"YearlyExp":YearlyExp,"monthlyyearly":monthlyyearly}
    return render(request,"gym/members.html",data)


@csrf_exempt
def members2(request):
    gmail=request.session['gmail']
    id=request.POST.get("id")
    book=Book.objects.get(gym=GymRegistration.objects.get(gmail=gmail),Bookid=id)
    plan=Workoutplan.objects.filter(Bookid=book)
    data={"data":book,"plan":plan}
    print("d")
    return render(request,"gym/members2.html",data)

import json

@csrf_exempt
def deleteplan(request):
    id=json.loads(request.body)["id"]
    try:
        print(id)
        plan=Workoutplan.objects.get(id=id)
        plan.delete()
    except Exception as e:
        pass
    data={}
    return JsonResponse(data,safe=False)


@csrf_exempt
def saveplan(request):
    id=json.loads(request.body)["bookid"]
    workoutDesc=json.loads(request.body)["workoutDesc"]
    workoutName=json.loads(request.body)["workoutName"]
    try:
        print(id)
        plan=Workoutplan.objects.create(Bookid=Book.objects.get(Bookid=id),workouts=workoutName,desc=workoutDesc)
    except Exception as e:
        pass
    data={}
    return JsonResponse(data,safe=False)



@csrf_exempt
def slots(request):
    gmail=request.session['gmail']
    gmail1=GymRegistration.objects.get(gmail=gmail)
    try:
        if request.POST:
            startTime=request.POST.get("startTime")
            endTime=request.POST.get("endTime")
            instructor=request.POST.get("instructor")
            Substitution=request.POST.get("Substitution")
            block=request.POST.get("block")
            if block!=None:
                ob2=Slot.objects.get(slotid=block)
                ob2.delete()
            ob=InstructorRegistration.objects.get(gmail=instructor)
            ob1=InstructorRegistration.objects.get(gmail=Substitution)
            id=None
            id=request.POST.get("id")
            print("detailssssssssssssssssssssssssssss")
            print(id,instructor,startTime,instructor,Substitution)
            if id==None and instructor!="Select" and Substitution!="Select" and block==None:
                Slot.objects.create(startTime=startTime,endTime=endTime,Gym=gmail1,instructor=ob,Substitution=ob1)
            elif id!=None and block==None:
                print("Dddddddddddddddddddddddddddddddddddddddfdgvfk")
                print(id)
                ob2=Slot.objects.get(slotid=id)
                ob2.startTime=startTime
                ob2.endTime=endTime
                ob2.instructor=ob
                ob2.Substitution=ob1
                ob2.save()

    except Exception as e:
        print(e)
    ob=Slot.objects.filter(Gym=gmail)
    data={}
    data["slots"]=ob
    data["job"]=Job.objects.filter(employer=gmail,staus=1)
    return render(request,"gym/slots.html",data)









@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('msg')
            user_name=request.POST.get('user_id')
            user_id=request.POST.get('user')
            print(user_id)
            user=request.session['gmail']
            ob=GymRegistration.objects.get(gmail=user)  
            
            if user_id=='1':
                print("sending message to admin")
                Feedback.objects.create(msg=message,Gym=ob,reciver_sts=4,sender_sts=3)
            elif user_id=='2':
                JJ=InstructorRegistration.objects.get(gmail=user_name)
                print("sending message to instructor")
                Feedback.objects.create(msg=message,instructor=JJ,reciver_sts=2,sender_sts=3,Gym=ob)
            elif user_id=='3':
                print("sending message to instructor")
                JJ=UserRegistration.objects.get(gmail=user_name)
                print("sending message to member")
                Feedback.objects.create(msg=message,user=JJ,reciver_sts=1,sender_sts=3,Gym=ob)
            return redirect("gym:feedback")
        except Exception as e:
            return redirect("gym:feedback")


    user=request.session['gmail']
    ob=GymRegistration.objects.get(gmail=user)
    feed=Feedback.objects.filter(Gym=ob)
    for i in feed:
        if i.reciver_sts==3:
            i.view_sts=1
            i.save()
    feed=Feedback.objects.filter(Gym=ob).order_by('-id')
    rating=Ratings.objects.filter(gym=ob).order_by('-id')
    data={"data":feed,"r":rating}
    return render(request,"gym/feedback.html",data)


@csrf_exempt
def Salary(request):
    return render(request,"gym/Salary.html")


@csrf_exempt
def Salary1(request):
    user=request.session['gmail']
    ob=GymRegistration.objects.get(gmail=user)  
    DATE=request.POST.get("date")
    print(DATE)
    data={}
    if DATE!="":
        target_date = datetime.strptime(DATE, "%Y-%m")
        bookings_in_target_month = Book.objects.filter(
            bookTime__year=target_date.year,
            bookTime__month=target_date.month
        )

        totalamt=0
        for i in bookings_in_target_month:
            sal=ob.month_rate
            if i.plan==1:
               totalamt=int(sal)+totalamt
            else:
                totalamt=(int(sal)*12)+totalamt

        totalpayment=totalamt
        InstructorRegistration
        lis=[]
        J=Job.objects.filter(employer=ob)
        totalsalary=0
        for i in J:
            objects_with_target_date = Attendance.objects.filter(date__year=target_date.year,date__month=target_date.month,Gym=ob,status=1,trainer=i.employe).first()
            if objects_with_target_date!=None:
                data={}
                data["gmail"]=i.employe.gmail
                data["name"]=i.employe.name
                jobsalary=i.salary
                data["salary"]=int(jobsalary)
                c=Attendance.objects.filter(Gym=ob,trainer=i.employe,date__year=target_date.year,date__month=target_date.month,status=1).count()
                data["totalattendence"]=c
                totalsalary=totalsalary+(int(jobsalary)*c)
                data["totalsal"]=int(jobsalary)*c
                lis.append(data)

        balance=totalpayment-totalsalary


        data={
            "payments":bookings_in_target_month,
            "salaries":lis,
            "totalpayment":totalpayment,
            "totalsalary":totalsalary,
            "totalamount":balance,
            "permonth":int(ob.month_rate),
            "peryear":int(ob.month_rate)*12
        }

    print(data)
    return render(request,"gym/Salary.html",data)
