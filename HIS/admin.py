from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Specialty)
admin.site.register(Doctor)
admin.site.register(Ward)
admin.site.register(IPDPatient)
admin.site.register(PatientDischarge)
admin.site.register(DeathSummary)
admin.site.register(OTSchedule)
admin.site.register(Login)