from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact_info = models.CharField(max_length=100)
    patient_type = [
        ('OPD', 'OPD'),
        ('IPD', 'IPD'),
        ('Emergency', 'Emergency'),
        ]
   
    patient_type = models.CharField(max_length=20, choices=patient_type)
    Date = models.DateField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True)


class Specialty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name



class IPDPatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    primary_consulting_doc = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, unique=True)
    consent_token = models.CharField(max_length=50, blank=True, null=True)
    loa = models.CharField(max_length=50, blank=True, null=True)
    disabilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patient.name



class PatientDischarge(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    discharge_type = models.CharField(max_length=50)
    discharge_date = models.DateField()
    discharged_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


class DeathSummary(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_code = models.CharField(max_length=20)
    patient_name = models.CharField(max_length=100)
    death_date = models.DateField()
    admission_no = models.CharField(max_length=20)
    confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.death_date}"




class OTSchedule(models.Model):
    
    surgery_name = models.CharField(max_length=100)
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    cvt_surgeon_name = models.CharField(max_length=100)
    perfusionist = models.CharField(max_length=100)
    surgery_code = models.CharField(max_length=100)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    anaesthesia_doctor_name = models.CharField(max_length=100)
    surgery_note = models.TextField()
    start_date = models.DateTimeField()   
    end_date = models.DateTimeField()
    surgery_for = models.CharField(max_length=100)
    estimate_time_of_surgery = models.CharField(max_length=50)
    patient_name = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,null=True)  
    

class Login(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
