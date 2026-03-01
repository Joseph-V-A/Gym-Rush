from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from Admin.models import Equipment


class UserRegistration(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    gmail = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    status=models.IntegerField(default=0)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class GymRegistration(models.Model):
    gym_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    instruments = models.ManyToManyField(Equipment)
    no_of_instructors = models.IntegerField(blank=True)
    documents=models.FileField(upload_to ='uploads/gym_docs', blank=True)
    gmail = models.EmailField(primary_key=True)
    month_rate=models.FloatField(default=500)
    password = models.CharField(max_length=255)
    status=models.IntegerField(default=0)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class InstructorRegistration(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    cv_and_documents = models.FileField(upload_to ='uploads/instructor', blank=True)
    gmail = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    current_gym_gmail = models.EmailField(blank=True)
    status=models.IntegerField(default=0)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)




class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    msg=models.CharField(max_length=100)
    user=models.ForeignKey(UserRegistration,null=True,on_delete=models.CASCADE)
    instructor=models.ForeignKey(InstructorRegistration,null=True,on_delete=models.CASCADE)
    Gym=models.ForeignKey(GymRegistration,null=True,on_delete=models.CASCADE)
    reciver_sts=models.IntegerField() # 1- User , 2- Instructor , 3- Gym , 4-Admin
    sender_sts=models.IntegerField() # 1- User , 2- Instructor , 3- Gym , 4-Admin
    view_sts=models.IntegerField(default=0)  # 1- view else not viewed