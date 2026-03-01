from django.urls import path
from . import views


app_name="instructor"

urlpatterns = [
path('home', views.home, name='home'),
path('profile', views.profile, name='profile'),
path('viewgyms', views.viewgyms, name='viewgyms'),
path('attendence', views.attendence, name='attendence'),
path('members', views.members, name='members'),
path('members2', views.members2, name='members2'),
path('members3', views.members3, name='members3'),
path('members4', views.members4, name='members4'),
path('apply_leave', views.apply_leave, name='apply_leave'),
path('attendenceMember', views.attendenceMember, name='attendenceMember'),
path('attendenceMember2', views.attendenceMember2, name='attendenceMember2'),
path('Apply/<str:gym>', views.Apply, name='Apply'),
path('offer/<int:id>', views.offer, name='offer'),
path('offer1/<int:id>', views.offer1, name='offer1'),
path('offer2/<int:id>', views.offer2, name='offer2'),
path('remove/<int:id>', views.remove, name='remove'),
path('feedback', views.feedback, name='feedback'),


path('Salary', views.Salary, name='Salary'),
path('Salary1', views.Salary1, name='Salary1'),
]
