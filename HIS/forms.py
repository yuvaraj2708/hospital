from django import forms
from .models import Appointment,Patient,PatientDischarge,DeathSummary,OTSchedule,Login
from django.contrib.auth.forms import AuthenticationForm

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'reason']

class IPDRegistrationForm(forms.ModelForm):
    speciality = forms.CharField(max_length=100)
    primary_consulting_doc = forms.CharField(max_length=100)
    ward = forms.CharField(max_length=50)
    barcode = forms.CharField(max_length=20, required=False)
    consent_token = forms.CharField(max_length=20, required=False)
    loa = forms.CharField(max_length=20, required=False)
    disabilities = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = Patient
        fields = ('name', 'age', 'gender', 'contact_info' , 'patient_type','Date' )


class PatientDischargeForm(forms.ModelForm):
    class Meta:
        model = PatientDischarge
        fields = ('patient_id', 'discharge_type', 'discharge_date', 'discharged_by')

class DeathSummaryForm(forms.ModelForm):
    class Meta:
        model = DeathSummary
        fields = ('patient_id','patient_code','patient_name','death_date','admission_no','confirm')



class OTScheduleForm(forms.ModelForm):
    class Meta:
        model = OTSchedule
        fields = ('surgery_name', 'speciality', 'cvt_surgeon_name', 'perfusionist', 'surgery_code', 'doctor_name', 'anaesthesia_doctor_name', 'surgery_note', 'start_date', 'end_date','surgery_for', 'estimate_time_of_surgery',  'patient_name')
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }


class FilterOTScheduleForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
   



class ApproveOTScheduleForm(forms.ModelForm):
    doctor_notes = forms.CharField(max_length=255, required=True)

    class Meta:
        model = OTSchedule
        fields = ['doctor_notes']
        



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)
