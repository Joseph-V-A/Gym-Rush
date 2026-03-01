from django.urls import path
from . import views
app_name = 'Admin'
urlpatterns = [
path('', views.home, name='home'),
path('view_gym', views.view_gym, name='view_gym'),
path('view_gym2', views.view_gym2, name='view_gym2'),
path('view_instructor', views.view_instructor, name='view_instructor'),
path('view_user', views.view_user, name='view_user'),
path('view_request', views.view_request, name='view_request'),
path('instruments', views.instruments, name='instruments'),
path('feedback', views.feedback, name='feedback'),
]
