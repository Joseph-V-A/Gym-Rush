from django.urls import path
from . import views

app_name = 'gym'
urlpatterns = [
        path('home', views.home, name='home'),
        path('profile', views.profile, name='profile'),
        path('attendence', views.attendence, name='attendence'),
        path('instructor', views.instructor, name='instructor'),
        path('CheckUsers', views.CheckUsers, name='CheckUsers'),
        path('remove_trainer/<str:gmail>', views.remove_trainer, name='remove_trainer'),
        path('sendoffer', views.sendoffer, name='sendoffer'),
        path('members', views.members, name='members'),
        path('members2', views.members2, name='members2'),
        path('deleteplan', views.deleteplan, name='deleteplan'),
         path('saveplan', views.saveplan, name='saveplan'),
        path('slots', views.slots, name='slots'),
        path('attendence2', views.attendence2, name='attendence2'),
        path('feedback', views.feedback, name='feedback'),

        path('Salary', views.Salary, name='Salary'),
        path('Salary1', views.Salary1, name='Salary1'),

         path('ApplicationAccept/<int:id>', views.ApplicationAccept, name='ApplicationAccept'),
         path('ApplicationAccept1', views.ApplicationAccept1, name='ApplicationAccept1'),
         path('ApplicationReject1', views.ApplicationReject1, name='ApplicationReject1'),
]
