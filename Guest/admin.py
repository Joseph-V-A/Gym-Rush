from django.contrib import admin
from .models import *
from django.conf import settings

# Register your models here.

admin.site.register(GymRegistration)
admin.site.register(InstructorRegistration)
admin.site.register(UserRegistration)