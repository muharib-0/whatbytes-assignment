from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'assigned_at')
    search_fields = ('patient__user__name', 'doctor__user__name')
    list_filter = ('assigned_at',)
    readonly_fields = ('assigned_at',)
    
    def get_patient_name(self, obj):
        return obj.patient.user.name
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.user.name
    get_doctor_name.short_description = 'Doctor'
