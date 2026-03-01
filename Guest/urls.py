from django.urls import path
from . import views

app_name = 'Guest'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='homepage'),
    path('gymreg', views.gymreg, name='gymreg'),
    path('gymreg2', views.gymreg2, name='gymreg2'),
    path('instreg', views.instreg, name='instreg'),
    path('userreg', views.userreg, name='userreg'),
    path('login/', views.login, name='login'),
    path('viewgyms', views.viewgyms, name='viewgyms'),
 path('otp', views.otp, name='otp'),
path('otp1', views.otp1, name='otp1'),
path('otp2', views.otp2, name='otp2'),

 path('otpp', views.otpp, name='otpp'),
path('otpp1', views.otpp1, name='otpp1'),
path('otpp2', views.otpp2, name='otpp2'),
path('forgotpassword', views.forgotpassword, name='forgotpassword'),
path('forgotpassword1/', views.forgotpassword1, name='forgotpassword1'),

path('forgotpassword2/', views.forgotpassword2, name='forgotpassword2'),

path('viewgyms', views.viewgyms, name='viewgyms'),
path('Gyms2/<str:gym>/<str:place>/<str:gym2>/', views.Gyms2, name='Gyms2'),

path('Gyms2/<str:gym>/<str:place>/', views.Gyms2, name='Gyms2_no_gym2'),

path('Gyms2/<str:gym>/<str:place>/<str:gym2>/', views.Gyms2, name='Gyms2_no_place'),

path('Gyms2/<str:gym>/', views.Gyms2, name='Gyms2_no_gym2_place'),



]
