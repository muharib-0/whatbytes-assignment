from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'age', 'gender', 'blood_group', 'created_at')
    search_fields = ('user__name', 'user__email', 'phone')
    list_filter = ('gender', 'blood_group', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_name(self, obj):
        return obj.user.name
    get_name.short_description = 'Name'
