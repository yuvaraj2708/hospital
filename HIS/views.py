from django.shortcuts import render,redirect
from .models import *
from django.db.models import Count
from .forms import AppointmentForm,IPDRegistrationForm,PatientDischargeForm
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.generic import ListView
from django.utils import timezone
from .models import DeathSummary,OTSchedule
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DeathSummaryForm,OTScheduleForm,ApproveOTScheduleForm,FilterOTScheduleForm
from xhtml2pdf import pisa
from datetime import timedelta, datetime
from django.shortcuts import render
from django.db.models import Q
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, Username=form.cleaned_data['username'], Password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard/')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    mymembers = Patient.objects.all()
    context = {
    'patient': mymembers,
    }
    ipd_count = Patient.objects.filter(patient_type='IPD').count()
    opd_count = Patient.objects.filter(patient_type='OPD').count()
    emergency_count = Patient.objects.filter(patient_type='Emergency').count()

    # Calculate the total count
    total_count = ipd_count + opd_count + emergency_count

    # Render the dashboard template with the counts
    return render(request, 'dashboard.html', {
        'ipd_count': ipd_count,
        'opd_count': opd_count,
        'emergency_count': emergency_count,
        'total_count': total_count
    })




   

def registration_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact_info = request.POST.get('contact_info')
        patient_type = request.POST.get('patient_type')
        Date = request.POST.get('Date')
        if name and age and gender and contact_info and patient_type and Date:
            patient = Patient(name=name, age=age, gender=gender, contact_info=contact_info, patient_type=patient_type,Date=Date)
            patient.save()
            return redirect('dashboard')
        else:
            # Handle form errors
            error_message = "Please fill in all required fields"
            return render(request, 'patient_registration.html', {'error_message': error_message})
    else:
        return render(request, 'frontdesk/patient_registration.html')




def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AppointmentForm()

    # retrieve all appointments from database
    appointments = Appointment.objects.all()

    return render(request, 'frontdesk/appointment.html', {'form': form, 'appointments': appointments})



def registrationsummary(request):
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    context = {
        'patients': patients,
        'appointments': appointments,
    }
    return render(request, 'frontdesk/registrationsummary.html', context)


def opd_dashboard(request):
    opd_count = Patient.objects.filter(patient_type='OPD').count()
    
    return render(request, 'outpatient/outdashboard.html', {
        'opd_count': opd_count,
    })

def opd_details(request):
    opd_patients = Patient.objects.filter(patient_type='OPD')
    context = {'opd_patients': opd_patients}
    
    return render(request, 'outpatient/OPDdetails.html', context)


def ipd_dashboard(request):
    patients = Patient.objects.all()
    context = {
        'patients': patients,
    }
    ipd_count = Patient.objects.filter(patient_type='IPD').count()
    
    return render(request, 'inpatient/inpatientdashboard.html', {
        'ipd_count': ipd_count,
    })


def ipd_details(request):
    ipd_patients = Patient.objects.filter(patient_type='IPD')
    context = {'ipd_patients': ipd_patients}
    
    return render(request, 'inpatient/ipddetails.html', context)




# def ipd_admission(request):
#     if request.method == 'POST':
#         form = IPDRegistrationForm(request.POST)
#         if form.is_valid():
#             patient = form.save(commit=False)
#             patient.patient_type = 'IPD'
#             patient.save()
#             ipd_registration = IPDPatient.objects.create(
#                 patient=patient,
#                 speciality=form.cleaned_data['speciality'],
#                 primary_consulting_doc=form.cleaned_data['primary_consulting_doc'],
#                 ward=form.cleaned_data['ward'],
#                 barcode=form.cleaned_data['barcode'],
#                 consent_token=form.cleaned_data['consent_token'],
#                 loa=form.cleaned_data['loa'],
#                 disabilities=form.cleaned_data['disabilities']
#             )
#             return redirect('inpatient/ipddetails.html', ipd_registration.id)
#     else:
#         form = IPDRegistrationForm()
#     return render(request, 'inpatient/ipd_admission.html', {'form': form})


def update(request, id):
       patients = Patient.objects.get(id=id)
       template = loader.get_template('inpatient/ipd_admission.html')
       context = {
       'patients': patients,
        }
       return HttpResponse(template.render(context, request))


def updaterecord(request, id):
    name = request.POST.get('name')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    contact_info = request.POST.get('contact_info')
    patient_type = request.POST.get('patient_type')
    Date = request.POST.get('Date')
    patient = Patient.objects.get(id=id)
    if name and age and gender and contact_info and patient_type and Date:
            patient = Patient(name=name, age=age, gender=gender, contact_info=contact_info, patient_type=patient_type,Date=Date)
            patient.save()
    
    return redirect('frontdesk/registrationsummary.html')



def patient_discharge(request):
    if request.method == 'POST':
        form = PatientDischargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discharge_summary')
    else:
        form = PatientDischargeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inpatient/patient_discharge.html', context)

def discharge_summary(request):
    patient_discharge = PatientDischarge.objects.all()
    context = {
        'patient_discharge': patient_discharge,
    }
    return render(request, 'inpatient/discharge_summary.html', context)


def download_discharge_summary(request):
    # get all patient discharge details
    patients = PatientDischarge.objects.all()

    # create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # create the PDF object, using the BytesIO object as its "file"
    p = canvas.Canvas(buffer)

    # draw the table headers
    p.drawString(50, 750, 'Patient ID')
    p.drawString(150, 750, 'Discharge Type')
    p.drawString(250, 750, 'Discharge Date')

    # draw the patient discharge details
    y = 700
    for patient in patients:
        p.drawString(50, y, str(patient.patient_id))
        p.drawString(150, y, patient.discharge_type)
        p.drawString(250, y, str(patient.discharge_date))
        y -= 20

    # close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # retrieve the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="patient_discharge_summary.pdf"'

    return response

from .models import DeathSummary

def death_entry(request):
    if request.method == 'POST':
        form = DeathSummaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('death_entry')
    else:
        form = DeathSummaryForm()
    
    # retrieve all DeathSummary objects from the database
    death_summary = DeathSummary.objects.all()
    
    context = {
        'form': form,
        'death_summary': death_summary,
    }
    return render(request, 'inpatient/death_entry.html', context)




def edit_death_summary(request, pk):
    # get death summary object by pk
    death_summary = get_object_or_404(DeathSummary, pk=pk)
    if request.method == 'POST':
        # update death summary object with new form data
        form = DeathSummaryForm(request.POST, instance=death_summary)
        if form.is_valid():
            form.save()
            return redirect('death_entry')
    else:
        form = DeathSummaryForm(instance=death_summary)
    context = {
        'form': form,
        'death_summary': death_summary,
    }
    return render(request, 'inpatient/edit_death_summary.html', context)




def delete_death_summary(request, pk):
    # get death summary object by id
    death_summary = get_object_or_404(DeathSummary, pk=pk)

    # delete death summary
    death_summary.delete()
    messages.success(request, 'Death Summary deleted successfully!')
    return redirect('death_entry')


def download_death_summary(request, id):
    death_summary = get_object_or_404(DeathSummary, id=id)
    template = get_template('inpatient/death_summary_pdf.html')
    context = {'death_summary': death_summary}
    html = template.render(context)
    pdf_file = HttpResponse(content_type='application/pdf')
    pdf_file['Content-Disposition'] = f'attachment; filename="{death_summary.patient_code}_death_summary.pdf"'
    pisa.CreatePDF(html, dest=pdf_file)
    return pdf_file




def emergency_dashboard(request):
    emergency_count = Patient.objects.filter(patient_type='Emergency').count()
    
    return render(request, 'emergency/emergencydashboard.html', {
        'emergency_count': emergency_count,
    })

def emergency_details(request):
    emergency_count = Patient.objects.filter(patient_type='Emergency')
    context = {'emergency_count': emergency_count}
    
    return render(request, 'emergency/emergencydetails.html', context)


def editemergency(request, pk):
    # get death summary object by pk
    editemergency = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        # update death summary object with new form data
        form = DeathSummaryForm(request.POST, instance=editemergency)
        if form.is_valid():
            form.save()
            return redirect('death_entry')
    else:
        form = DeathSummaryForm(instance=editemergency)
    context = {
        'form': form,
        'editemergency': editemergency,
    }
    return render(request, 'emergency/editemergency.html', context)

def add_ot_schedule(request):
    if request.method == 'POST':
        form = OTScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_ot_schedule')
    else:
        form = OTScheduleForm()
    return render(request, 'OT/add_ot_schedule.html', {'form': form})


def approve_ot_schedule(request, pk):
    ot_schedule = get_object_or_404(OTSchedule, pk=pk)

    if request.method == 'POST':
        form = ApproveOTScheduleForm(request.POST, instance=ot_schedule)
        if form.is_valid():
            ot_schedule = form.save(commit=False)
            ot_schedule.status = 'Approved' 
            ot_schedule.save()
            return redirect('schedule_ot')
    else:
        form = ApproveOTScheduleForm(instance=ot_schedule)

    return render(request, 'OT/approve_ot_schedule.html', {'form': form})


 

def schedule_ot(request):
    if request.method == 'POST':
        form = OTScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_ot')
    else:
        form = OTScheduleForm()
    return render(request, 'OT/schedule_ot.html', {'form': form})


def filter_ot_schedule(request):
    if request.method == 'POST':
        form = FilterOTScheduleForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            filtered_schedules = OTSchedule.objects.filter(
                start_date__gte=start_date,
                status='Approved'
            )
            return render(request, 'OT/schedule_ot.html', {'schedules': filtered_schedules})
    else:
        form = FilterOTScheduleForm()
        return render(request, 'OT/schedule_ot.html', {'form': form})
