from django.contrib import admin

# Register your models here.
from .models import *
from django.conf import settings


admin.site.register(Workoutplan)
admin.site.register(Job)
admin.site.register(Slot)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Book)
admin.site.register(SlotBooking)