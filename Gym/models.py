from django.db import models
from Guest.models import *
# Create your models here.
from datetime import *

class Job(models.Model):
    employe=models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE)
    employer=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    salary=models.IntegerField()
    staus=models.IntegerField()

class Slot(models.Model):
    slotid=models.AutoField(primary_key=True)
    startTime=models.CharField(max_length=50)
    endTime=models.CharField(max_length=50)
    Gym=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    seats=models.IntegerField(default=10)
    instructor=models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE,related_name='instructor_slots')
    Substitution=models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE,related_name='substitution_slots')


class Attendance(models.Model):  # trainer attendencetbl
    Gym=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)    
    trainer = models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField()


class Leave(models.Model):
    to=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    trainer = models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE)
    subject=models.CharField(max_length=500)
    body=models.CharField(max_length=1000)
    date= models.DateField()
    status=models.IntegerField(default=0)


class Book(models.Model):
    Bookid=models.AutoField(primary_key=True)
    cust=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    gym=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    slot=models.ForeignKey(Slot,on_delete=models.CASCADE,null=True)
    plan=models.IntegerField()  # 1--> MONTLY  2--> YEARLY
    bookTime=models.DateTimeField(auto_now=True)
    Startdate=models.DateField()
    EndDate=models.DateField()
    def status(self):
        if self.EndDate and self.EndDate < datetime.now().date():
            return 0 
        else:
            return 1 


class Workoutplan(models.Model):
    Bookid=models.ForeignKey(Book,on_delete=models.CASCADE)
    workouts=models.TextField(max_length=1000)   
    desc=models.TextField(max_length=100)
    remarkByTrainer=models.TextField(max_length=100,default="No remark added")
    status=models.IntegerField(default=0) 


class SlotBooking(models.Model):
    bookid=models.ForeignKey(Book,on_delete=models.CASCADE)
    Slotid=models.ForeignKey(Slot,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.IntegerField(default=0)



class Ratings(models.Model):
    user=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    gym=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    star=models.IntegerField()
    comment=models.CharField(max_length=100)

class JobApplication(models.Model):
    instructor=models.ForeignKey(InstructorRegistration,on_delete=models.CASCADE)
    gym=models.ForeignKey(GymRegistration,on_delete=models.CASCADE)
    comment=models.CharField(max_length=100,null=True)
    status=models.IntegerField(default=0) # 0- applied , 1-accept and give offer , 2- rejected
