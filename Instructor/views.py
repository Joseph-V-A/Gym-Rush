from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from Guest.models import *
from Admin.models import *
from Gym.models import *
# Create your views here.
from django.db.models import Q
from django.http import JsonResponse


@csrf_exempt
def home(request):
    instructor_email = request.session["gmail"]
    jb=Job.objects.filter(employe=InstructorRegistration.objects.get(gmail=instructor_email),staus=0)
    jk=JobApplication.objects.filter(instructor=InstructorRegistration.objects.get(gmail=instructor_email),status__in=[0, 2])
    return render(request,"trainer/home.html",{"name":InstructorRegistration.objects.get(gmail=instructor_email).name,"jb":jb,"jt":jk})



@csrf_exempt
def remove(request,id):
    j=JobApplication.objects.filter(id=id).first()
    j.delete()
    return redirect("instructor:home")



@csrf_exempt
def offer(request,id):
    jb=Job.objects.filter(id=id).first()
    return render(request,"trainer/offers.html",{"jb":jb})    

@csrf_exempt
def offer1(request,id):
    instructor_email = request.session["gmail"]
    jk=Job.objects.filter(employe=InstructorRegistration.objects.get(gmail=instructor_email),staus=1).first()
    if jk!=None:
        jk.staus=3
        jk.save()

    jb=Job.objects.filter(id=id).first()
    jb.staus=1
    jb.save()
    return redirect("instructor:home")


@csrf_exempt
def offer2(request,id):
    jb=Job.objects.filter(id=id).first()
    jb.staus=2
    jb.save()
    return redirect("instructor:home")


@csrf_exempt
def Apply(request,gym):
    instructor_email = request.session["gmail"]
    instructor = InstructorRegistration.objects.get(gmail=instructor_email)
    g=GymRegistration.objects.filter(gmail=gym).first()
    JobApplication.objects.create(instructor=instructor,gym=g)
    return redirect("instructor:home")



@csrf_exempt
def profile(request):
    instructor_email = request.session["gmail"]
    instructor = InstructorRegistration.objects.get(gmail=instructor_email)
    current_gym1=Job.objects.filter(employe=instructor,staus=1).first()
    current_gym=0
    if current_gym1!=None:
        current_gym=current_gym1.employer.gym_name

    if request.method == 'POST':
        instructor.name = request.POST.get('name')
        instructor.gender = request.POST.get('gender')
        #instructor.current_gym_gmail = request.POST.get('current_gym_gmail')
        #instructor.status = request.POST.get('status')
        if request.FILES.get('cv_and_documents'):
            instructor.cv_and_documents = request.FILES['cv_and_documents']
        instructor.save()
        return redirect('instructor:profile')  # Redirect to the same page after updating

    context = {
        'instructor': instructor,
        'current_gym':current_gym
    }
    return render(request,"trainer/profile.html",context)



@csrf_exempt
def viewgyms(request):
    try:
        if request.POST:            
            if request.POST.get("place")!="" and request.POST.get("gym")!="":
                ob=GymRegistration.objects.filter(place__iexact=request.POST.get("place"),gym_name__iexact=request.POST.get("gym"),status=1)
                data={"data":ob}
                data["place"]=request.POST.get("place")
                data["gym"]=request.POST.get("gym")
                return render(request,"trainer/searchgym.html",data)
            elif request.POST.get("place")!="":
                print("place")
                ob=GymRegistration.objects.filter(status=1,place__iexact=request.POST.get("place"))
                data={"data":ob}
                data["place"]=request.POST.get("place")
                return render(request,"trainer/searchgym.html",data)
            elif request.POST.get("gym")!="":
                print("gym")
                ob=GymRegistration.objects.filter(status=1,gym_name__iexact=request.POST.get("gym"))
                data={"data":ob}
                data["gym"]=request.POST.get("gym")
                return render(request,"trainer/searchgym.html",data)

    except Exception as e:
        print(e)
    ob=GymRegistration.objects.filter(status=1)
    data2=[]
    for i in ob:
        count = Job.objects.filter(staus=1, employer=i).count()
        data2.append("No vacany avalible" if i.no_of_instructors-count==0 else i.no_of_instructors-count)
    zipping=zip(ob,data2)
    data={"data":zipping}
    print(ob)
    return render(request,"trainer/searchgym.html",data)


@csrf_exempt
def Gyms2(request):
    return render(request,"trainer/searchgym.html",data)

@csrf_exempt
def attendence(request):
    try:
        instructor_email = request.session["gmail"]
        attendance_records = Attendance.objects.filter(trainer__gmail=instructor_email).order_by('-date')
        Leave1=Leave.objects.filter(trainer=instructor_email).order_by('-id')
        data={}
        data["data"]=attendance_records
        data["leave"]=Leave1
        #print(data)
        print(data["data"])
        return render(request,"trainer/attendence.html",data)
    except Exception as e:
        return render(request,"trainer/attendence.html")



@csrf_exempt
def attendenceMember(request):
    try:
        if request.POST.get("date"):
            date=request.POST.get("date")
            print(date)
            date_str = date  # Define the date string
            date = datetime.strptime(date_str, '%Y-%m-%d')  # Parse the date string into a datetime object
            
            if datetime.now() >= date:
                gmail=request.session['gmail']
                instid=InstructorRegistration.objects.get(gmail=gmail)
                job=Job.objects.filter(employe=instid,staus=1).first()
                Slots = Slot.objects.filter(Gym=job.employer).filter(Q(instructor=instid) | Q(Substitution=instid))
                data=[]
                for i in Slots:
                    print(i)
                    bookings=Book.objects.filter(gym=job.employer,EndDate__gte=datetime.now().date(),plan=2,slot=i.slotid)
                    for j in bookings:
                        try:
                            ob=SlotBooking.objects.get(date=date,bookid=j,Slotid=i)
                        except Exception as e:
                            ob=SlotBooking.objects.create(date=date,bookid=j,Slotid=i)

                    slt=SlotBooking.objects.filter(date=date,Slotid=i)
                    print("slt is",slt)
                    for m in slt:
                        data1={
                            "id":m.id,
                            "name":m.bookid.cust.name,
                            "gmail":m.bookid.cust.gmail,
                            "Date":m.date,
                            "status": m.status
                        }
                        data.append(data1)
                    
                data={"data":data}
                print(data)
                return JsonResponse(data,safe=False)
            data={"data":"0"}
            print("problem")
            return JsonResponse(data,safe=False)
    except Exception as e:
        return JsonResponse({},safe=False)

@csrf_exempt
def attendenceMember2(request):
    slotid = request.POST.get("employee_id")
    status = request.POST.get("status")
    try:
        if request.POST:
            k=SlotBooking.objects.get(id=slotid)
            k.status=status
            k.save()
            print("attendence")
        
    except Exception as e:
        pass
    data={}
    return JsonResponse(data,safe=False)


from django.contrib import messages

def apply_leave(request):
    try:
        if request.method == 'POST':
            subject = request.POST.get('subject')
            date = request.POST.get('date')
            reason = request.POST.get('reason')
            trainer_email = request.session.get("gmail")
            trainer_email1=InstructorRegistration.objects.get(gmail=trainer_email)
            gym_mail_find=Job.objects.get(employe=trainer_email,staus=1)
            gym_mail=GymRegistration.objects.get(gmail=gym_mail_find.employer.gmail)
            Leave.objects.create(trainer=trainer_email1,to=gym_mail,subject=subject, body=reason,date=date)
            messages.success(request, 'Leave application submitted successfully.')
        return redirect('instructor:attendence')
    except Exception as e:
        return redirect('instructor:attendence')

from django.db.models import Q
@csrf_exempt
def members(request):
    try:
        gmail=request.session['gmail']
        instid=InstructorRegistration.objects.get(gmail=gmail)
        job=Job.objects.filter(employe=instid,staus=1).first()


        Slots = Slot.objects.filter(Gym=job.employer).filter(Q(instructor=instid) | Q(Substitution=instid))
        print(Slots)
        bookings1=[]
        bookings2=[]
        yearly=[]
        for i in Slots:
            bookings=Book.objects.filter(gym=job.employer,EndDate__gte=datetime.now().date(),plan=2,slot=i.slotid)
            for j in bookings:
                bookings1.append(j)
            bookingss=SlotBooking.objects.filter(Slotid=i.slotid,date=datetime.now().date())
            for k in bookingss:
                bookings2.append(Book.objects.get(Bookid=k.bookid.Bookid))
        new=[]
        new.extend(bookings1)
        new.extend(bookings2)
        print(bookings2)
        data={"Yearly":bookings1,"monthly":bookings2,"monthlyyearly":new}

        return render(request,"trainer/members.html",data)
    except Exception as e:
        return render(request,"trainer/members.html")


@csrf_exempt
def members2(request):
    id=request.POST.get("id")
    book=Book.objects.get(Bookid=id)
    plan=Workoutplan.objects.filter(Bookid=book)
    data={"data":book,"plan":plan}
    print("d")
    return render(request,"trainer/members2.html",data)


import json
@csrf_exempt
def members3(request):
    id=json.loads(request.body)["id"]
    try:
        print(id)
        plan=Workoutplan.objects.get(id=id)
        plan.status=1
        plan.save()
    except Exception as e:
        print(e)
    data={}
    return JsonResponse(data,safe=False)    

@csrf_exempt
def members4(request):
    id=json.loads(request.body)["id"]
    msg=json.loads(request.body)["msg"]
    try:
        print(msg)
        plan=Workoutplan.objects.get(id=id)
        plan.remarkByTrainer=msg
        plan.save()
    except Exception as e:
        print(e)
    data={}
    return JsonResponse(data,safe=False)    
@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        message = request.POST.get('msg')
        
        user_id=request.POST.get('user')
        print(user_id)
        user=request.session['gmail']
        ob=InstructorRegistration.objects.get(gmail=user)  
        job=Job.objects.filter(employe=ob,staus=1).last()
        if user_id=='1':
            print("sending message to admin")
            Feedback.objects.create(msg=message,instructor=ob,reciver_sts=4,sender_sts=2)
        elif user_id=='2':
            print("sending message to gym")
            Feedback.objects.create(msg=message,instructor=ob,reciver_sts=3,sender_sts=2,Gym=job.employer)
        return redirect("instructor:feedback")


    user=request.session['gmail']
    ob=InstructorRegistration.objects.get(gmail=user)
    Bookk=Job.objects.filter(employe=ob,staus=1).last()
    gym=0
    if Bookk!=None:
        gym=Bookk.employer.gym_name
    data={"gym":gym}
    feed=Feedback.objects.filter(instructor=ob)
    for i in feed:
        if i.reciver_sts==2:
            i.view_sts=1
            i.save()
    feed=Feedback.objects.filter(instructor=ob).order_by('-id')
    data={"data":feed}
    return render(request,"trainer/feedback.html",data)





@csrf_exempt
def Salary(request):
    return render(request,"trainer/Salary.html")


@csrf_exempt
def Salary1(request):
    user=request.session['gmail']
    ob=InstructorRegistration.objects.get(gmail=user)  
    DATE=request.POST.get("date")
    print(DATE)
    data={}
    if DATE!="":
        target_date = datetime.strptime(DATE, "%Y-%m")
        bookings_in_target_month = Book.objects.filter(
            bookTime__year=target_date.year,
            bookTime__month=target_date.month
        )
       
        lis=[]
        J=Job.objects.filter(employe=ob)
        for i in J:
            objects_with_target_date = Attendance.objects.filter(date__year=target_date.year,date__month=target_date.month,Gym=i.employer,status=1,trainer=ob).first()
            if objects_with_target_date!=None:
                data={}
                data["gmail"]=i.employer.gmail
                data["name"]=i.employer.gym_name
                jobsalary=i.salary
                data["salary"]=int(jobsalary)
                c=Attendance.objects.filter(Gym=i.employer,trainer=i.employe,date__year=target_date.year,date__month=target_date.month,status=1).count()
                data["totalattendence"]=c
                data["totalsal"]=int(jobsalary)*c
                lis.append(data)



        data={
            "salaries":lis,
        }

    print(data)
    return render(request,"trainer/Salary.html",data)
