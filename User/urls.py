from django.urls import path
from . import views

app_name="User"

urlpatterns = [
path('home', views.home, name='home'),
path('profile', views.profile, name='profile'),
path('Gyms', views.Gyms, name='Gyms'),
path('Gyms3', views.Gym3, name='Gyms3'),
path('Gyms2/<str:gym>/<str:place>/<str:gym2>/', views.Gyms2, name='Gyms2'),

path('Gyms2/<str:gym>/<str:place>/', views.Gyms2, name='Gyms2_no_gym2'),

path('Gyms2/<str:gym>/<str:place>/<str:gym2>/', views.Gyms2, name='Gyms2_no_place'),

path('Gyms2/<str:gym>/', views.Gyms2, name='Gyms2_no_gym2_place'),

path('back', views.back, name='back'),
path('my_workout_plain', views.my_workout_plain, name='my_workout_plain'),
path('slot', views.slot, name='slot'),

path('feedback', views.feedback, name='feedback'),
path('feedback1', views.feedback1, name='feedback1'),

]
