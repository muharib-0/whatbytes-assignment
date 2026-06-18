from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'specialization', 'experience_years', 'created_at')
    search_fields = ('user__name', 'user__email', 'specialization', 'phone')
    list_filter = ('specialization', 'experience_years', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_name(self, obj):
        return obj.user.name
    get_name.short_description = 'Name'
