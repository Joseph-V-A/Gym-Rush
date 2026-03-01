from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['trainer', 'status']
        widgets = {
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class DateSelectionForm(forms.Form):
    attendance_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'attendanceDateInstructors'}))
